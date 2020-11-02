from django.db import models
from rest_framework import serializers

from users.models import BeforeMatch

class BMSerializer(serializers.ModelSerializer):
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(auto_now=True)
    class Meta:
        model = BeforeMatch
        fields = '__all__'