from django.db import models
from users.models import User


class Team(models.Model):
    username = models.ManyToManyField(User, related_name='team_user')


class Match(models.Model):
    team_pk = models.ManyToManyField(Team, related_name='match_team')
    sports = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Locations(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    sports = models.CharField(max_length=30)
    lat = models.FloatField()
    lng = models.FloatField()
