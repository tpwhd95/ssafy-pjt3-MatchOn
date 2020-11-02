from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
    # 최대 매치 개수를 생각해서 제한할 것
    bm_match = BeforeMatch(
        user = request.user, 
        status = 1, 
        sports_name = data['sports_name'],
        # DateTimeField 데이터 형식 : 2019-05-08T09:23:09.424129Z
        start_time = '2019-05-08T09:23:09.424129Z',
        end_time = '2019-05-08T09:23:09.424129Z',
        lat = data['lat'],
        lng = data['lng']
         )
    bm_match.save()
    return Response(status=status.HTTP_200_OK)