# from django.db import models
from djongo import models
from users.models import User


class Sports(models.Model):
    sportname = models.CharField(max_length=10)


class Match(models.Model):
    sport_pk = models.ForeignKey(Sports, on_delete=models.CASCADE)
    users = models.ArrayField(model_container=User)
    teams = models.ArrayField(model_container=Team)
    locations = models.ArrayField(model_container=Locations)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)


class Team(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    class Meta:
        abstract = True

    
class Team_User(models.Model):
    team_pk = models.ForeignKey(Team, on_delete=models.CASCADE)
    user_pk = models.IntegerField()


class Locations(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    sports = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    class Meta:
        abstract = True