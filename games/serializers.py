from rest_framework import serializers
from .models import BoardGames, GameDetails

class BoardGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardGames
        fields = '__all__'

class GameDetailsSerializer(serializers.ModelSerializer):
    boardgame = BoardGamesSerializer(read_only=True)
    class Meta:
        model = GameDetails
        fields = '__all__'
