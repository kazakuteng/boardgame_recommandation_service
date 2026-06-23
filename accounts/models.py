from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    profile_image = models.FileField(upload_to='profiles/', blank=True)
    favorite_games = models.ManyToManyField('games.BoardGames', blank=True, related_name='fans')
