from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators

class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    social_id = models.CharField(max_length=50)


class BeforeMatch(models.Model):
    # 스테이터스는 매칭의 진행과정으로 '1: 매칭 전', '2: 매칭 중', '3: 매칭 확정(장소 및 시간 픽스와 경기 중까지)', '4: 게임 중', '5: 게임 종료(전적 확인용 데이터)', '성사되지 못한 매치'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    # 스포츠PK
    sports_name = models.CharField(max_length=20)
    # 경기 하고 싶은 시간
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # 위치
    lat = models.FloatField()
    lng = models.FloatField()
    gu = models.CharField(max_length=50, null=True)
    device_token = models.CharField(max_length=255, null=True, blank=True)


class AfterMatch(models.Model):
    before_match = models.ForeignKey(BeforeMatch, on_delete=models.CASCADE)
    matching_pk = models.IntegerField()
    team_pk = models.IntegerField(null=True)
    fixed_time = models.TimeField(null=True, blank=True)
    fixed_lat = models.FloatField(null=True, blank=True)
    fixed_lng = models.FloatField(null=True, blank=True)
    result = models.BooleanField(null=True, blank=True)