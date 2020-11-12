from django.shortcuts import render, get_object_or_404

import requests
import json
from django.forms.models import model_to_dict
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_auth.registration.views import SocialLoginView
import hashlib

from .models import User, BeforeMatch, AfterMatch
from match.models import Match, MatchUser
from .serializers import UserSerializer,UserSerializerWithToken

class KakaoLogin(SocialLoginView):
    def post(self, request):
        url = "https://kapi.kakao.com/v2/user/me"
        json_data = json.loads(requests.get(url,headers={'Authorization':'Bearer '+request.data['access_token']}).text)
        print(json_data)
        u = User.objects.filter(social_id=json_data['id'])
        if not u:
            username1 = ''.join(json_data['properties']['nickname'].split())
            user = User(username=username1, social_id=json_data['id'], password=json_data['id'])
            serializer = UserSerializerWithToken(data = model_to_dict(user))
            if serializer.is_valid():
                serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        user = User.objects.get(id = u[0].id)
        user.social_id = 0
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def match_info(request):
    user = request.user
    all_bms = BeforeMatch.objects.filter(user=request.user).order_by('-date', '-start_time')
    data = []
    for bm in all_bms:
        match_dict = {}
        match_dict['status'] = bm.status
        match_dict['sports_name'] = bm.sports_name
        match_dict['date'] = bm.date
        match_dict['start_time'] = bm.start_time
        match_dict['end_time'] = bm.end_time
        match_dict['gu'] = bm.gu
        if int(bm.status) >= 2:
            am = get_object_or_404(AfterMatch, before_match=bm.pk)
            match_dict['matching_pk'] = am.matching_pk
            match_dict['match_start'] = get_object_or_404(Match, pk=am.matching_pk).start_time
            match_dict['match_end'] = get_object_or_404(Match, pk=am.matching_pk).end_time
            match_dict['team_pk'] = am.team_pk
            match_dict['fixed_time'] = am.fixed_time
            match_dict['fixed_lat'] = am.fixed_lat
            match_dict['fixed_lng'] = am.fixed_lng
            match_dict['result'] = am.result

        data.append(match_dict)
    context = {
        'result' : 'true',
        'data' : data
    }
    return Response(context, status=status.HTTP_200_OK)