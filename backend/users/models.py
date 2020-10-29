from django.db import models
# from djongo import models
from django.contrib.auth.models import AbstractUser
# from match.models import Team


class User(AbstractUser):
    user_id = models.CharField(max_length=64, primary_key=True)
    nickname = models.CharField(max_length=50)
    social_id = models.CharField(max_length=50)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    # bowling_win = models.IntegerField(default=0)
    # bowling_lose = models.IntegerField(default=0)
    # bowling_average = models.IntegerField(default=0)
    # pool_win = models.IntegerField(default=0)
    # pool_lose = models.IntegerField(default=0)
    # pool_average = models.IntegerField(default=0)
    # soccer_win = models.IntegerField(default=0)
    # soccer_lose = models.IntegerField(default=0)
    # basketball_win = models.IntegerField(default=0)
    # basketball_lose = models.IntegerField(default=0)
    # tennis_win = models.IntegerField(default=0)
    # tennis_lose = models.IntegerField(default=0)