import json
import urllib.request, urllib.parse, urllib.error
from urllib.parse import quote
from .variable_data import *
from .config import create_unverified_context

ctx = create_unverified_context()

# https://api.neople.co.kr/df/servers/<serverId>/characters/<characterId>/equip/equipment?apikey=IvIirUYlTIIqIHY199xUB0lgOGCVNyY4

def get_item_info(server_id, cha_id):
    item_url1 = "https://api.neople.co.kr/df/servers/"
    item_server = server_id + "/characters/"
    item_url2 = cha_id + "/equip/equipment?apikey=IvIirUYlTIIqIHY199xUB0lgOGCVNyY4"

    item_url = item_url1 + item_server + item_url2

    # URL 열기
    item_result = urllib.request.urlopen(item_url, context=ctx).read()

    item_info = json.loads(item_result)

    # 주어진 값들
    Custom_list = Custom_epic_list

    # 주어진 값들이 나온 횟수의 총합을 저장할 변수
    Custom_epic = 0

    # 주어진 값들이 나온 횟수 세기
    for i in range(0, len(item_info['equipment'])): #장착 장비의 길이를 구해서, 장비가 벗겨진 상태인 경우 범위 오류가 날 수 있음.
        item_name = item_info['equipment'][i]['itemName']
        for user_item in Custom_list:
            if user_item in item_name:
                Custom_epic += 1

    # 결과 출력
    #print(f"커스텀 에픽 개수 : {Custom_epic}")

    #print("============== 미스트 기어 있는지 검출하기 테스트, 세트아이템이름 기준. =============")

    # 주어진 값들
    mistGear = ['안개를 걷는 자 세트']

    # 주어진 값들이 나온 횟수의 총합을 저장할 변수
    mistGear_count = 0

    # 주어진 값들이 나온 횟수 세기
    for i in range(0, len(item_info['equipment'])): #장착 장비의 길이를 구해서, 장비가 벗겨진 상태인 경우 범위 오류가 날 수 있음.
        setItemName = item_info['equipment'][i].get('setItemName')  # setItemName이 None인지 확인
        if setItemName is not None and mistGear[0] in setItemName:  # setItemName이 None이 아니고, 값이 존재하는 경우에만 확인
            mistGear_count += 1

    # 결과 출력
    #print(f"보유 미스트기어 개수 : {mistGear_count}")

    item_level_sum = 0
    for item in item_info['equipment']:
        if 'fixedOption' in item and 'level' in item['fixedOption']:
            #print(item['slotName'], item['fixedOption']['level'])
            if '仙' in item['itemName']: #선계 업그레이드 된 장비만을 추출하기
                item_level_sum += item['fixedOption']['level']
        elif 'customOption' in item and 'level' in item['customOption']:
            #print(item['slotName'], item['customOption']['level'])
            if '仙' in item['itemName']:
                item_level_sum += item['customOption']['level']

    #print(f"장비 성장 레벨 총합 : {item_level_sum}")

    return Custom_epic, mistGear_count, item_level_sum


