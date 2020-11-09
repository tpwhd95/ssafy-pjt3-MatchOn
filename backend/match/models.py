from django.db import models
# from djongo import models
# from users.models import User, Team


class Sports(models.Model):
    sports_name = models.CharField(max_length=100)
    def __str__(self):
        return self.sports_name


class Match(models.Model):
    sports = models.ForeignKey(Sports, on_delete=models.CASCADE)
    # 장소
    # 시간


class MatchUser(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user_pk = models.IntegerField()
    team = models.BooleanField(null=True)

# 경기장 위치
class Locations(models.Model):
    sports = models.ForeignKey(Sports, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    gu_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    tel = models.CharField(max_length=200, null=True)
    # 공공시설만 해당하는 데이터
    url = models.TextField(null=True)