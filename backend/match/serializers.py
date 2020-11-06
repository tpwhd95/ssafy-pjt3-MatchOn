from django.db import models
from rest_framework import serializers

from users.models import BeforeMatch

class BMSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeforeMatch
        fields = '__all__'