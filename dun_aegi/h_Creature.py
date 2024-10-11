import json
import urllib.request, urllib.parse, urllib.error
import ssl
from urllib.parse import quote
from .config import create_unverified_context
#import variable_data
from .variable_data import *

ctx = create_unverified_context()

def get_creature(server_id, cha_id):
    creature_url1 = "https://api.neople.co.kr/df/servers/"
    creature_server = server_id + "/characters/"
    creature_url2 = cha_id + "/equip/creature?apikey=IvIirUYlTIIqIHY199xUB0lgOGCVNyY4"

    creature_url = creature_url1 + creature_server + creature_url2

    # URL 열기
    creature_result = urllib.request.urlopen(creature_url, context=ctx).read()

    creature_info = json.loads(creature_result)

    #print(creature_info)

    #print(creature_info['creature']['itemName']) #크리쳐 이름 꺼내기

    # 주어진 조건을 만족하는지 확인
    wearing_creature = creature_info['creature']['itemName']
    #print(wearing_creature)
    Queen_creature_IS = Queen_creature_list

    # 풀네임이 아니여도, 가끔 패스같은 이름이 붙을 수 있으니까, 특정 단어만 들어가도 되게 끔 설정
    if any(name in wearing_creature for name in Queen_creature_IS):
        #print('Y')
        Queen_creature = "Y"
    else:
        #rint('N')
        Queen_creature = "N"
    
    return Queen_creature