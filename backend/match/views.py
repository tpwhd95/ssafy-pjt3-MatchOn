from django.shortcuts import render, get_object_or_404
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
        # 날짜 표기 방식
        # "date":"2020-11-04"
        # "start_time":"14:57:18.091261"
        # "end_time":"14:57:18.091261"

        # 테스트용 데이트 자료
        # date = '2020-11-04',
        # start_time = '15:21:32',
        # end_time = '15:21:32',
        date = datetime.date.today(),
        start_time = (datetime.datetime.now() - datetime.timedelta(hours= 3)).strftime("%H:%M"),
        end_time = datetime.datetime.now().time(),

        # date = data['date'],
        # start_time = data['start_time'],
        # end_time = data['end_time'],

        lat = data['lat'],
        lng = data['lng'],
        gu = re_geocode(data['lat'], data['lng'])
         )
    bm_match.save()
    serializer = BMSerializer(bm_match)


    # 첫 번째 탐색법
    # 매칭 전 / 종목 이름 / 날짜 / 구 이름이 같은 조건 탐색
    # crnt_bm_matches = BeforeMatch.objects.filter(status = 1, sports_name = bm_match.sports_name, date = bm_match.date, gu = bm_match.gu).exclude(user = bm_match.user)
    # sports_count = {'tennis': 2, 'pool': 2, 'bowl': 2, 'basket_ball': 6, 'futsal': 12}
    
    # # 해당 스포츠의 같은 동네에서 인원 수가 충족되고
    # if crnt_bm_matches.count() >= sports_count[bm_match.sports_name] - 1:
    #     # 시간도 겹치는지 확인해봅시다.
    #     match_users = [set() for _ in range(24)]
    #     # 현재 사용자의 정보를 집어넣고
    #     stime_idx = int(bm_match.start_time[:2])
    #     etime_idx = int(bm_match.end_time.strftime("%H:%M")[:2])
        
    #     for i in range(stime_idx, etime_idx + 1):
    #         match_users[i].add(bm_match.pk)
        
    #     matched = []
    #     # 다른 사람들의 정보를 집어넣는다.
    #     for user_bm in crnt_bm_matches.order_by('pk'):
    #         stime_idx = int(user_bm.start_time.strftime("%H:%M")[:2])
    #         etime_idx = int(user_bm.end_time.strftime("%H:%M")[:2])
            
    #         for i in range(stime_idx, etime_idx + 1):
    #             if len(match_users[i]) >= sports_count[bm_match.sports_name] - 1:
    #                 print(match_users[i])
    #                 # matched.append(match_users[i])
    #                 # 현재 넣고 있는 유저의 넣었던 내용 빼기

    #                 # 매칭된 유저의 내용 빼기
    #             else:
    #                 match_users[i].add(user_bm.pk)
    # else:
    #     print('Naah')


    # 두 번째 탐색법 -> 모두 찾기!
    crnt_bm_matches = BeforeMatch.objects.filter(status = 1, sports_name = bm_match.sports_name, date = bm_match.date, gu = bm_match.gu)
    sports_count = {'tennis': 2, 'pool': 2, 'bowl': 2, 'basket_ball': 6, 'futsal': 12}
    
    # 해당 스포츠의 같은 동네에서 인원 수가 충족되고
    if crnt_bm_matches.count() >= sports_count[bm_match.sports_name]:
        # 시간도 겹치는지 확인해봅시다.
        match_users = [set() for _ in range(24)]
        matched = []
        # 다른 사람들의 정보를 집어넣는다.
        for user_bm in crnt_bm_matches.order_by('pk'):
            stime_idx = int(user_bm.start_time.strftime("%H:%M")[:2])
            etime_idx = int(user_bm.end_time.strftime("%H:%M")[:2])
            
            for i in range(stime_idx, etime_idx + 1):
                # 해당 시간대;match_users[i]의 인원이 
                if len(match_users[i]) >= sports_count[bm_match.sports_name] - 1:
                    print('match_users[i]: ', match_users[i])
                    import copy
                    matched_users = copy.deepcopy(match_users[i])
                    
                    # 현재 유저까지 추가해서 매칭된 유저에 넣어서 매칭된 게임에 전달해준다.
                    match_users[i].add(user_bm.pk)
                    # 매칭된 게임 정보는 matched에 넣어준다.
                    matched.append(match_users[i])
                    
                    print('matched: ', matched)
                    # 매칭된 유저의 내용 빼기
                    for user_pk in matched_users:
                        matched_user_bm = BeforeMatch(pk=user_pk)
                        print('matched_user_bm: ', matched_user_bm)
                        print(matched_user_bm.start_time)
                        # s_idx = int(matched_user_bm.start_time.strftime("%H:%M")[:2])
                        # e_idx = int(matched_user_bm.end_time.strftime("%H:%M")[:2])

                        # print(s_idx, e_idx)
                        # for j in range(s_idx, e_idx + 1):
                        #     match_users[j].remove(user_pk)
                    # 현재 넣고 있는 유저의 넣었던 내용 빼기

                else:
                    match_users[i].add(user_bm.pk)
            # print(match_users)
            # print(matched)
    else:
        print('Naah')


    return Response(serializer.data, status=status.HTTP_200_OK)

