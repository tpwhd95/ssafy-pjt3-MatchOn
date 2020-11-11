from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# 외부함수
from .match_funcs import re_geocode

# 모델
from users.models import User, BeforeMatch, AfterMatch
from match.models import Sports, Match, MatchUser, Locations

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
    # 시간 겹치지 않게 처리

    all_user_bm = BeforeMatch.objects.filter(user=request.user, date = data['date']).exclude(Q(status= '4') | Q(status='5'))
    
    stime_str = data['start_time']
    stime = datetime.datetime.strptime(stime_str, '%H:%M').time()

    etime_str = data['end_time']
    etime = datetime.datetime.strptime(etime_str, '%H:%M').time()

    if all_user_bm:
        for user_bm in all_user_bm:
            if etime < user_bm.start_time or stime > user_bm.end_time:
                continue
            else:
                msg = {"status_code": 403, "detail": "이미 해당 시간에 매칭 중인 게임이 있습니다."}
                return Response(msg)

    bm_match = BeforeMatch(
        user = request.user, 
        status = 1, 
        sports_name = data['sports_name'],
        date = data['date'],
        start_time = data['start_time'],
        end_time = data['end_time'],
        lat = data['lat'],
        lng = data['lng'],
        gu = re_geocode(data['lat'], data['lng']),
        device_token = data['device_token']
        )
    bm_match.save()
    serializer = BMSerializer(bm_match)


    # 매칭 전 / 종목 이름 / 날짜 / 구 이름이 같은 조건 탐색
    crnt_bm_matches = BeforeMatch.objects.filter(status = 1, sports_name = bm_match.sports_name, date = bm_match.date, gu = bm_match.gu)
    sports_count = {'tennis': 2, 'pool': 2, 'bowl': 2, 'basket_ball': 6, 'futsal': 12}
    
    # 해당 스포츠의 같은 동네에서 인원 수가 충족되고
    if crnt_bm_matches.count() >= sports_count[bm_match.sports_name]:
        # 시간도 겹치는지 확인해봅시다.
        match_users = [[] for _ in range(24)]
        matched = []
        # 다른 사람들의 정보를 집어넣는다.

        for user_bm in crnt_bm_matches.order_by('pk'):
            stime_idx = int(user_bm.start_time.strftime("%H:%M")[:2])
            etime_idx = int(user_bm.end_time.strftime("%H:%M")[:2])
            
            for i in range(stime_idx, etime_idx + 1):
                if len(match_users[i]) >= sports_count[bm_match.sports_name] - 1:                    
                    import copy
                    matched_users = copy.deepcopy(match_users[i])
                    # 매칭된 유저의 내용 빼기
                    match_stime = datetime.time(hour=00, minute=00)
                    match_etime = datetime.time(hour=23, minute=59)
                    for user_pk in matched_users:
                        crnt_bm = get_object_or_404(BeforeMatch, pk=user_pk)
                        s_idx = int(crnt_bm.start_time.strftime("%H:%M")[:2])
                        e_idx = int(crnt_bm.end_time.strftime("%H:%M")[:2])

                        if match_stime < crnt_bm.start_time:
                            match_stime = crnt_bm.start_time
                        if match_etime > crnt_bm.end_time:
                            match_etime = crnt_bm.end_time

                        for j in range(s_idx, e_idx + 1):
                            match_users[j].remove(user_pk)

                    if match_stime < user_bm.start_time:
                        match_stime = user_bm.start_time
                    if match_etime > user_bm.end_time:
                        match_etime = user_bm.end_time

                    # 현재 유저까지 추가해서 매칭된 유저에 넣어서 매칭된 게임에 전달해준다.
                    # 매칭된 게임 정보는 matched에 넣어준다.
                    matched_users.append(user_bm.pk)
                    matched_users.append(match_stime)
                    matched_users.append(match_etime)
                    matched.append(matched_users)
                    # 현재 넣고 있는 유저의 넣었던 내용 빼기
                    for k in range(stime_idx, i):
                        match_users[k].remove(user_bm.pk)                        
                    break
                else:
                    match_users[i].append(user_bm.pk)
        # 잡혀진 매치가 있다면 해당 매치를 게임으로 바꿔줘야겠죠.
        tokens = {}
        while matched:
            # BeforeMatch PK가 들어가 있는 리스트
            bm_pks = matched.pop()
            bm_etime = bm_pks.pop()
            bm_stime = bm_pks.pop()
            # 매치를 잡아줍니다.
            sports_name = get_object_or_404(Sports, sports_name=bm_match.sports_name)
            match = Match(sports = sports_name)
            match.date = bm_match.date
            match.start_time = bm_stime
            match.end_time = bm_etime
            match.save()

            # 유저 정보를 꺼내서 AfterMatch와 MatchUser를 만들어 줍니다.
            for idx, bm_pk in enumerate(bm_pks):
                bm = get_object_or_404(BeforeMatch, pk=bm_pk)
                bm.status = 2
                bm.save()
                
                tokens[bm.user.pk] = bm.device_token

                # MatchUser를 저장해줍니다.
                mmatch_user = MatchUser(
                    match = match,
                    user_pk = bm.user.pk
                )
                if idx % 2:
                    mmatch_user.team = 1
                else:
                    mmatch_user.team = 0
                mmatch_user.save()

                # AfterMatch를 만들어줍니다.
                am = AfterMatch(
                    before_match = bm,
                    matching_pk = match.pk
                )
                am.save()
        context = {
            'result': 'true',
            'device_tokens': tokens,
        }
        return Response(context, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def match_room(request):
    data = request.data
    match = get_object_or_404(Match, pk = data['match_pk'])
    match_users = MatchUser.objects.filter(match = match.pk)
    # 장소 정보 넣어서 보내기
    locations = Locations.objects.filter(sports = match.sports)

    users = {}
    for user in match_users:
        users[user.user_pk] = {
            'nickname': get_object_or_404(User, pk=user.user_pk).nickname, 
            'team': user.team
            }

    res = [
        {
        'match_pk': match.pk,
        'date': match.date, 
        'start_time': match.start_time, 
        'end_time': match.end_time,
        'users': users,
        'locations': {}
        }
    ]

    context = {
        'result' : 'true',
        'data': res
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(['POST'])
def after_match(request):
    # 팀 / 시간 / 장소를 확정하고 각 플레이어들의 데이터를 저장해준다.
    data = request.data
    match = get_object_or_404(Match, pk=data['match_pk'])

    match.fixed_time = data.fixed_time
    match.save()
    match_users = MatchUser.objects.filter(match=match.pk)
    for match_user in match_users:
        print(match_user)
    return Response(status=status.HTTP_200_OK)