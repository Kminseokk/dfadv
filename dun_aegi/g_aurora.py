import json
import urllib.request, urllib.parse, urllib.error
from urllib.parse import quote
from .config import create_unverified_context
#import variable_data
from .variable_data import *

ctx = create_unverified_context()

def get_aurora (server_id, cha_id):
    avatar_url1 = "https://api.neople.co.kr/df/servers/"
    avatar_server = server_id + "/characters/"
    avatar_url2 = cha_id + "/equip/avatar?apikey=IvIirUYlTIIqIHY199xUB0lgOGCVNyY4"

    avatar_url = avatar_url1 + avatar_server + avatar_url2

    # URL 열기
    avatar_result = urllib.request.urlopen(avatar_url, context=ctx).read()

    avatar_info = json.loads(avatar_result)

    # 주어진 조건을 만족하는지 확인
    wearing_ora = next((avatar['itemName'] for avatar in avatar_info['avatar'] if avatar['slotId'] == 'AURORA'), None)

    fashionista_name_IS = fashionista_name_list

    # 풀네임이 아니여도, 가끔 패스같은 이름이 붙을 수 있으니까, 특정 단어만 들어가도 되게 끔 설정, noun 값 예외 처리
    if wearing_ora is not None:
        if any(name in wearing_ora for name in fashionista_name_IS):
            fashionista_aurora = "Y"
        else:
            fashionista_aurora = "N"
    else:
        fashionista_aurora = "N"
        
    return fashionista_aurora