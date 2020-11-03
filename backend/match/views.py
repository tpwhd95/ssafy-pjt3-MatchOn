from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# 외부함수
from .match_funcs import re_geocode

# 모델
from users.models import BeforeMatch

# 시리얼라이저
from .serializers import BMSerializer

# 임시로 사용하는 데코레이터입니다.
# from .models import 

# 매칭 등록 시 
@api_view(['POST'])
def before_match(request):
    data = request.data

    import datetime

    # 최대 매치 개수를 생각해서 제한할 것
    bm_match = BeforeMatch(
        user = request.user, 
        status = 1, 
        sports_name = data['sports_name'],
        # DateTimeField 데이터 형식 : 2019-05-08T09:23:09.424129Z
        # start_time = '2019-05-08T09:00:00',
        start_time = datetime.datetime.now() - datetime.timedelta(days = 2),
        end_time = datetime.datetime.now(),
        lat = data['lat'],
        lng = data['lng'],
        gu = re_geocode(data['lat'], data['lng'])
         )
    bm_match.save()
    serializer = BMSerializer(bm_match)

    crnt_bm_matches = BeforeMatch.objects.filter(status = 1, sports_name = bm_match.sports_name, gu = bm_match.gu).exclude(user = bm_match.user)
    sports_count = {'tennis': 2, 'pool': 2, 'bowl': 2, 'basket_ball': 6, 'futsal': 12}
    
    # 해당 스포츠의 같은 동네에서 인원 수가 충족되고
    if crnt_bm_matches.count() >= sports_count[bm_match.sports_name] - 1:
        # 시간도 겹치는지 확인해봅시다.
        match_users = []
        for user in crnt_bm_matches.order_by('pk'):
            pass
            # if user.start_time <= bm_match.start_time
        print('Yeah!')
    else:
        print('Naah')

    return Response(serializer.data, status=status.HTTP_200_OK)

