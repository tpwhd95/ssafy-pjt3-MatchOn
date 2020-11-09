import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "backend.settings") 
import django 
django.setup()

from match.models import Locations


with open('public.json', 'rt', encoding='UTF8') as f:
    json_data_public = json.load(f)

with open('park.json', 'rt', encoding='UTF8') as f:
    json_data_park = json.load(f)

with open('reserve.json', 'rt', encoding='UTF8') as f:
    json_data_reserve = json.load(f)

# print(json.dumps(json_data_1, ensure_ascii=False, indent='\t'))
# print(json.dumps(json_data_park, ensure_ascii=False, indent='\t'))
# print(json.dumps(json_data_sports, ensure_ascii=False, indent='\t'))
place = []
p_list = ['풋살장', '풋살경기장', '농구장', '농구경기장', '테니스장', '테니스경기장']
s_list = ['풋살', '농구', '테니스']

aa = json_data_public["DATA"]
bb = json_data_park["DATA"]
cc = json_data_reserve["DATA"]

# 공공체육시설
for i in aa:
    kk = i['spt_kind'].split()
    pl = []
    for z in kk:
        if z in s_list:
            pl.append(z)
        if z[:-1] in s_list:
            pl.append(z)
    for z in pl:
        if z in p_list:
            tem = {
                "name" : i['nm'],
                "gu_name" : i['gu_nm'],
                "spt_kind" : pl,
                # "spt_kind" : i['spt_kind'],
                "lat" : i['ycode'],
                "lng" : i['xcode'],
                "address" : i['addr'],
                "tel" : i['tel'],
                "url" : i['home_page'],
                "img" : None,
                "str" : None,
                "end" : None,
            }
            place.append(tem)




# 공원
for i in bb:
    k = str(i['main_equip']).split()
    pl = []
    for z in k:
        for s in s_list:
            if s in z:
                # if z[-1]==',':
                #     pl.append(z[:-2])
                # else:
                #     pl.append(z[:-1])
                pl.append(s)
    if len(pl) != 0:
        tem = {
            "name" : i['p_park'],
            "gu_name" : i['p_zone'],
            "spt_kind" : pl,
            # WGS84
            "lat" : i['latitude'],
            "lng" : i['longitude'],
            "address" : i['p_addr'],
            "tel" : i['p_admintel'],
            "url" : i['template_url'],
            "img" : i['p_img'],
            "str" : None,
            "end" : None,
        }
    place.append(tem)



# 운동시설
for i in cc:
    if i['minclassnm'] in p_list:
        tem = {
            "name" : i['placenm'],
            "gu_name" : i['areanm'],
            "spt_kind" : [i['minclassnm'][:-1]],
            "lat" : i['y'],
            "lng" : i['x'],
            "address" : i['svcnm'],
            "tel" : i['telno'],

            # 공공시설에만 해당 함
            "url" : i['svcurl'],
            "img" : i['imgurl'],
            "str" : i['v_min'],
            "end" : i['v_max'],

        }
        place.append(tem)


print(type(place)) # 하나 둘 셋 이진석 화이팅!

url_list = []
place_list = []
for p in place:
    if p['spt_kind'] == ['풋살경기']:
        p['spt_kind'] = ['풋살']
    print(p['spt_kind'])
    if p['url'] not in url_list:
        url_list.append(p['url'])
        place_list.append(p)


print(place_list)


with open('place.json', 'w', encoding='UTF-8' ) as place_file:
    json.dump(place_list , place_file, ensure_ascii=False)

cnt = 0
for _  in place_list:
    cnt += 1
print(cnt)

model_instances = [Locations(
    name=record['name'],
    lat=record['lat'],
    lng=record['lng'],
    gu_name=record['gu_name'],
    address=record['address'],
    tel=record['tel'],
    url=record['url'],
    sports_id=1
) for record in place_list]

Locations.objects.all().delete()
Locations.objects.bulk_create(model_instances)



# import requests
# from bs4 import BeautifulSoup
# from pprint import pprint


# url = 'https://yeyak.seoul.go.kr/reservation/view.web?rsvsvcid='
# response = requests.get(url + 'S201030102944573871').text
# # print(response)
# data = BeautifulSoup(response, 'html.parser')
# # print(data)

# parse_url = '#contents > div.infoArea > div.calArea'

# reserve = data.select(parse_url)
# print('@@@@@@@@@@@@@@@@')
# print(reserve)
