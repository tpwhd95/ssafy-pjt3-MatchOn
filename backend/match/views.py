from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Prefetch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# 외부함수
from .match_funcs import re_geocode, re_dongcode

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
    sports_count = {'tennis': 2, 'pool': 2, 'bowling': 2, 'basket_ball': 6, 'futsal': 12}
    
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
        
        if not matched:
            return Response(serializer.data, status=status.HTTP_200_OK)

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

            lat_sum = 0
            lng_sum = 0
            # 유저 정보를 꺼내서 AfterMatch와 MatchUser를 만들어 줍니다.
            for idx, bm_pk in enumerate(bm_pks):
                bm = get_object_or_404(BeforeMatch, pk=bm_pk)
                bm.status = 2
                bm.save()
                
                # 중간 위치를 위한 위도 경도 계산
                lat_sum += bm.lat
                lng_sum += bm.lng

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
            match.lat = lat_sum / len(bm_pks)
            match.lng = lng_sum / len(bm_pks)
            match.save()
        context = {
            'result': 'true',
            'device_tokens': tokens,
        }
        return Response(context, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def match_room(request):
    data = request.data
    match = get_object_or_404(Match, pk = data['match_pk'])
    match_users = MatchUser.objects.filter(match = match.pk)
    # 장소 정보 넣어서 보내기
    locations = Locations.objects.filter(sports = match.sports)

    users = {}
    for user in match_users:
        am = get_object_or_404(AfterMatch, matching_pk=match.pk, before_match__user=user.user_pk)
        bm = am.before_match
        users[user.user_pk] = {
            'username': get_object_or_404(User, pk=user.user_pk).username, 
            'team': user.team,
            'lat': bm.lat,
            'lng': bm.lng
            }

    res = [
        {
        'sports': match.sports.sports_name,
        'match_pk': match.pk,
        'date': match.date, 
        'match_lat': match.lat,
        'match_lng': match.lng,
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

    match.fixed_time = data['fixed_time']
    match.save()
    for user in data['users']:
        match_user = get_object_or_404(MatchUser, match=match, user_pk=user)
        match_user.team = data['users'][user]['team']
        match_user.save()

        am = get_object_or_404(AfterMatch, before_match__user=user, matching_pk=match.pk)
        bm = am.before_match
        bm.status = '3'
        bm.save()
        
        am.fixed_time = data['fixed_time']
        am.team_pk = data['users'][user]['team']
        """
        공간정보는 업데이트 필요
        """
        am.fixed_lat = data['fixed_lat']
        am.fixed_lng = data['fixed_lng']
        am.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def result(request):
    user = request.user
    data = request.data
    if data['result'] == 'true':
        result = True
    elif data['result'] == 'false':
        result = False
    
    match = get_object_or_404(Match, pk=data['match_pk'])
    result_writer = get_object_or_404(MatchUser, match=match.pk, user_pk=user.pk)
    team = result_writer.team
    flag = 0
    if match.won_team == None:
        if team == True:
            match.won_team = result
            match.zero_resulted = True
            match.save()
        elif team == False:
            if result == True:
                match.won_team = False
                match.save()
            elif result == False:
                match.won_team = True
                match.save()
            match.one_resulted = True
            match.save()
        context = {
            'result': 'ready',
            'detail': '다른 팀의 결과 입력을 기다리고 있습니다.'
        }
        return Response(context, status=status.HTTP_200_OK)
    
    if team == True: # True 팀일 때
        if match.zero_resulted == True:
            context = {
                'result': 'error',
                'detail': '이미 결과를 투표하셨습니다.'
            }
            return Response(context, status=status.HTTP_200_OK)
        if result != match.won_team:
            flag = 1
        match.zero_resulted = True
        match.save()
    elif team == False: # False 팀일 때
        if match.one_resulted == True:
            context = {
                'result': 'error',
                'detail': '이미 결과를 투표하셨습니다.'
            }
            return Response(context, status=status.HTTP_200_OK)
        if result == match.won_team:
            flag = 1
        match.one_resulted = True
        match.save()
    
    if flag:
        match.won_team = None
        match.one_resulted = False
        match.zero_resulted = False
        match.save()
        context = {
            'result': 'false',
            'detail': '양팀의 게임 결과가 일치하지 않습니다. 결과를 다시 입력해주세요.'
        }
        return Response(context, status=status.HTTP_200_OK)

    match_users = MatchUser.objects.filter(match=match)
    for match_user in match_users:
        am = get_object_or_404(AfterMatch, before_match__user=match_user.user_pk, matching_pk=match.pk)
        bm = am.before_match
        bm.status = '5'
        bm.save()

        if match.won_team == match_user.team:
            am.result = True
            am.save()
        else:
            am.result = False
            am.save()
    context = {
        'result': 'true',
        'datail': f'팀 번호 {int(match.won_team)}의 승리결과에 대한 처리가 완료되었습니다.'
    }
    return Response(context, status=status.HTTP_200_OK)

@api_view(['GET'])
def report(request):
    user = get_object_or_404(User, username=request.user)
    context = {}
    sports = ['pae_ssaum', 'futsal', 'basket_ball', 'bowling', 'tennis', 'pool']
    for i in range(1, 6):
        match_count = AfterMatch.objects.filter(before_match__user=user, before_match__status='5', before_match__sports_name=sports[i]).count()
        win_match_count = AfterMatch.objects.filter(before_match__user=user, before_match__status='5', before_match__sports_name=sports[i], result=True).count()
        lose_match_count = match_count - win_match_count
        temp = {}
        temp['win'] = win_match_count
        temp['lose'] = lose_match_count
        temp['total'] = match_count
        if match_count != 0:
            temp['rate'] = round((win_match_count / match_count) * 100, 2)
        else:
            temp['rate'] = round(0, 2)
        temp['sports_id'] = i
        temp['sports_name'] = sports[i]
        context[sports[i]] = temp
    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
def report_detail(request, sports_pk):
    user = get_object_or_404(User, username=request.user)
    print(user)
    sports = ['pae_ssaum', 'futsal', 'basket_ball', 'bowling', 'tennis', 'pool']
    sports_kr = ['pae_ssaum', '풋살', '농구', '볼링', '테니스', '당구']
    result_kr = ['패배', '승리']
    matches = AfterMatch.objects.filter(before_match__user=user, before_match__sports_name=sports[int(sports_pk)], before_match__status='5')
    context = []
    for match in matches:
        temp = {}
        temp['id'] = match.id
        temp['date'] = match.before_match.date
        temp['sports_name'] = sports_kr[int(sports_pk)]
        temp['fixed_time'] = match.fixed_time
        temp['gu'] = re_dongcode(match.fixed_lat, match.fixed_lng)
        temp['result'] = result_kr[int(match.result)]
        context.append(temp)
    return Response(context, status=status.HTTP_200_OK)