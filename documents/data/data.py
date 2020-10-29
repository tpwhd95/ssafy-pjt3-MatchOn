import json
import os


current = os.getcwd()

with open(current + '\\documents\\data\\public.json', 'rt', encoding='UTF8') as f:
    json_data_public = json.load(f)

with open(current + '\\documents\\data\\park.json', 'rt', encoding='UTF8') as f:
    json_data_park = json.load(f)

with open(current + '\\documents\\data\\sports.json', 'rt', encoding='UTF8') as f:
    json_data_sports = json.load(f)

# print(json.dumps(json_data_1, ensure_ascii=False, indent='\t'))
# print(json.dumps(json_data_park, ensure_ascii=False, indent='\t'))
# print(json.dumps(json_data_sports, ensure_ascii=False, indent='\t'))
place = []
p_list = ['풋살장', '농구장', '테니스장']
s_list = ['풋살', '농구', '테니스']

aa = json_data_public["DATA"]
bb = json_data_park["DATA"]
cc = json_data_sports["DATA"]

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
                if z[-1]==',':
                    pl.append(z[:-1])
                else:
                    pl.append(z)

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
        print([i['minclassnm']])
        tem = {
            "name" : i['placenm'],
            "gu_name" : i['areanm'],
            "spt_kind" : [i['minclassnm']],
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


print(place)
cnt = 0
for _  in place:
    cnt += 1
print(cnt)