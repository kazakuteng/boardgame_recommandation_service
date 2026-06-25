import csv
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from games.models import BoardGames, GameDetails


DETAILS_CSV_PATH = "data/game_details.csv"
RANKS_CSV_PATH = "boardgames_ranks.csv"


def deployment_detail_targets():
    csv_path = Path(settings.BASE_DIR) / DETAILS_CSV_PATH
    if not csv_path.exists():
        return 3000, 0

    detail_count = 0
    korean_title_count = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            detail_count += 1
            if str(row.get("korean_title") or "").strip():
                korean_title_count += 1
    return detail_count, korean_title_count


class Command(BaseCommand):
    help = "Seed deployment database with ranked games and detail stats when data is missing."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Run imports even when data already exists.")

    def handle(self, *args, **options):
        force = options["force"]
        game_count = BoardGames.objects.count()
        detail_count = GameDetails.objects.count()
        korean_title_count = BoardGames.objects.exclude(korean_title="").count()
        expected_detail_count, expected_korean_title_count = deployment_detail_targets()

        if force or game_count < 3000:
            self.stdout.write("Seeding BoardGames from boardgames_ranks.csv...")
            call_command("import_boardgames_from_csv", path=RANKS_CSV_PATH, limit=3000)
        else:
            self.stdout.write(f"BoardGames already seeded: {game_count}")

        if (
            force
            or detail_count < expected_detail_count
            or korean_title_count < expected_korean_title_count
        ):
            self.stdout.write("Seeding GameDetails and Korean titles from data/game_details.csv...")
            call_command("import_game_details", path=DETAILS_CSV_PATH)
        else:
            self.stdout.write(f"GameDetails already seeded: {detail_count}, Korean titles: {korean_title_count}")

        missing_image_count = BoardGames.objects.filter(
            rank__gt=0,
            rank__lte=3000,
            thumbnail_url="",
            image_url="",
        ).count()
        if missing_image_count and getattr(settings, "BGG_TOKEN", ""):
            self.stdout.write(f"Fetching {missing_image_count} missing BGG image(s)...")
            call_command(
                "fetch_game_details",
                all=True,
                missing_images=True,
                sleep=0.5,
                max_retries=2,
            )
        elif missing_image_count:
            self.stdout.write(
                self.style.WARNING(
                    f"Missing BGG images: {missing_image_count}. Set BGG_TOKEN to fetch them."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Seed check complete: "
                f"BoardGames={BoardGames.objects.count()}, "
                f"KoreanTitles={BoardGames.objects.exclude(korean_title='').count()}, "
                f"GameDetails={GameDetails.objects.count()}"
            )
        )
