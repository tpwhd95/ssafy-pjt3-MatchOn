from django.shortcuts import render

import requests
import json
from django.forms.models import model_to_dict
from django.http import HttpResponse
from .models import User
from .serializers import UserSerializer,UserSerializerWithToken

from rest_auth.registration.views import SocialLoginView
from rest_framework.response import Response
from rest_framework import status
import hashlib


class KakaoLogin(SocialLoginView):
    def post(self, request):
        url = "https://kapi.kakao.com/v2/user/me"
        json_data = json.loads(requests.get(url,headers={'Authorization':'Bearer '+request.data['access_token']}).text)
        print(json_data)
        u = User.objects.filter(social_id=json_data['id'])
        if not u:
            # enc = hashlib.md5()
            # enc.update(str(json_data['id']).encode('utf-8'))
            # encText = enc.hexdigest()
            # user = User(id = encText, username=json_data['properties']['nickname'], social_id=json_data['id'], password=json_data['id'])
            username = ''.join(json_data['properties']['nickname'].split())
            user = User(username=username, social_id=json_data['id'], password=json_data['id'])
            serializer = UserSerializerWithToken(data = model_to_dict(user))
            if serializer.is_valid():
                serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        user = User.objects.get(id = u[0].id)
        # user = u[0]
        user.social_id = 0
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)