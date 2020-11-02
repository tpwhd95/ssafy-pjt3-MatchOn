from django.db import models
from django.contrib.auth.models import AbstractUser
# from djongo import models
# from match.models import Team


class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    social_id = models.CharField(max_length=50)


class BeforeMatch(models.Model):
    # 스테이터스는 매칭의 진행과정으로 '매칭 전', '매칭 중', '매칭 확정(장소 및 시간 픽스와 경기 중가지)', '게임 종료', '성사되지 못한 매치'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    # 스포츠PK
    sports_name = models.IntegerField()
    # 경기 하고 싶은 시간
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # 위치
    lat = models.FloatField()
    lng = models.FloatField()


class AfterMatch(models.Model):
    before_match = models.ForeignKey(BeforeMatch, on_delete=models.CASCADE)
    matching_pk = models.IntegerField()
    team_pk = models.IntegerField(null=True)
    fixed_time = models.DateTimeField(null=True, blank=True)
    fixed_lat = models.FloatField(null=True, blank=True)
    fixed_lng = models.FloatField(null=True, blank=True)
    result = models.BooleanField(null=True, blank=True)