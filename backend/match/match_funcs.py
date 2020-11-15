# 좌표 -> 위치 반환 코드
def re_geocode(lat, lng):
    import requests, json

    KEY = '0df3f7aca34fb1536a4fb5964fac74d2'
    
    URL = f'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={lng}&y={lat}'
    headers = {"Authorization": 'KakaoAK' + ' ' + KEY}
    result = json.loads(str(requests.get(URL, headers=headers).text))
    
    si_name = result['documents'][0]['region_1depth_name']
    gu_name = result['documents'][0]['region_2depth_name']

    full_gu = si_name + '_' + gu_name
    return full_gu

def re_dongcode(lat, lng):
    import requests, json

    KEY = '0df3f7aca34fb1536a4fb5964fac74d2'
    
    URL = f'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={lng}&y={lat}'
    headers = {"Authorization": 'KakaoAK' + ' ' + KEY}
    result = json.loads(str(requests.get(URL, headers=headers).text))
    dong_name = result['documents'][0]['address_name']
    return dong_name




def test_func():
    import time
    print ("10초만 잘래요")
    time.sleep(10)
    print("일어났어요!")
    return