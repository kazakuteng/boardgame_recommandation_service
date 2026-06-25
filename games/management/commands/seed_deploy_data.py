from django.core.management import call_command
from django.core.management.base import BaseCommand

from games.models import BoardGames, GameDetails


class Command(BaseCommand):
    help = "Seed deployment database with ranked games and detail stats when data is missing."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Run imports even when data already exists.")

    def handle(self, *args, **options):
        force = options["force"]
        game_count = BoardGames.objects.count()
        detail_count = GameDetails.objects.count()
        korean_title_count = BoardGames.objects.exclude(korean_title="").count()

        if force or game_count < 3000:
            self.stdout.write("Seeding BoardGames from boardgames_ranks.csv...")
            call_command("import_boardgames_from_csv", path="boardgames_ranks.csv", limit=3000)
        else:
            self.stdout.write(f"BoardGames already seeded: {game_count}")

        if force or detail_count < 3000 or korean_title_count < 2000:
            self.stdout.write("Seeding GameDetails and Korean titles from data/game_details.csv...")
            call_command("import_game_details", path="data/game_details.csv")
        else:
            self.stdout.write(f"GameDetails already seeded: {detail_count}, Korean titles: {korean_title_count}")

        self.stdout.write(
            self.style.SUCCESS(
                "Seed check complete: "
                f"BoardGames={BoardGames.objects.count()}, "
                f"KoreanTitles={BoardGames.objects.exclude(korean_title='').count()}, "
                f"GameDetails={GameDetails.objects.count()}"
            )
        )
