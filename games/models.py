from django.db import models

class BoardGames(models.Model):
    game_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    rank = models.IntegerField()
    released_year = models.IntegerField()
    view_count = models.IntegerField(default=0)

class GameDetails(models.Model):
    boardgame = models.ForeignKey(BoardGames, on_delete=models.CASCADE, related_name='details')
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    playing_time = models.IntegerField()
    weight = models.FloatField()