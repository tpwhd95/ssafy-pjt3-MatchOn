from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.CharField(max_length=64, primary_key=True)
    nickname = models.CharField(max_length=50)
    social_id = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    bowling_win = models.IntegerField()
    bowling_lose = models.IntegerField()
    bowling_average = models.IntegerField()
    pool_win = models.IntegerField()
    pool_lose = models.IntegerField()
    pool_average = models.IntegerField()
    soccer_win = models.IntegerField()
    soccer_lose = models.IntegerField()
    basketball_win = models.IntegerField()
    basketball_lose = models.IntegerField()
    tennis_win = models.IntegerField()
    tennis_lose = models.IntegerField()