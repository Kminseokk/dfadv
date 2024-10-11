import json
import urllib.request, urllib.parse, urllib.error
from urllib.parse import quote
from .config import create_unverified_context
#import variable_data
from .variable_data import *

ctx = create_unverified_context()

def get_siv_N_title(server_id, cha_id):
    item_url1 = "https://api.neople.co.kr/df/servers/"
    item_server = server_id + "/characters/"
    item_url2 = cha_id + "/equip/equipment?apikey=IvIirUYlTIIqIHY199xUB0lgOGCVNyY4"

    item_url = item_url1 + item_server + item_url2

    # URL 열기
    item_result = urllib.request.urlopen(item_url, context=ctx).read()

    item_info = json.loads(item_result)

    #print("아이템 인포 ", item_info)
    #print(len(item_info['equipment']))

    enchant_info = None

    for item in item_info['equipment']:
        if item['slotId'] == 'SUPPORT':
            enchant_info = item['enchant']
            break

    #enchant_info = item_info['equipment'][10]['enchant']
    #noun이 아닐때만 실행
    if enchant_info is not None:
        has_siv = any(info['name'] == '모든 속성 강화' and info['value'] == 12 for info in enchant_info['status'])
        
        # 결과 출력
        if has_siv:
            siv_enchant = "Y"
        else:
            siv_enchant = "N"
    else:
        siv_enchant = "N"

    # 칭호 확인 
    wearing_title = None

    for item in item_info['equipment']:
        if item['slotId'] == 'TITLE':
            wearing_title = item['itemName']
            break

    #wearing_title = item_info['equipment'][1]['itemName']

    #print("확인용#############################",enchant_info, wearing_title)
    awakening_title_IS = awakening_title_name_list

    # 풀네임이 아니여도, 가끔 패스같은 이름이 붙을 수 있으니까, 특정 단어만 들어가도 되게 끔 설정
    if any(name in wearing_title for name in awakening_title_IS):
        #print('Y')
        awakening_title = "Y"
    else:
        #print('N')
        awakening_title = "N"
    
    return siv_enchant, awakening_title
