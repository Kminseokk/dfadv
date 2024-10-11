import json
import urllib.request, urllib.parse, urllib.error
from urllib.parse import quote
from .config import create_unverified_context
from .variable_data import *

def adv_check(input_adventure, input_server, input_name):
    ctx = create_unverified_context()

    url1 = "https://api.neople.co.kr/df/servers/"
    server = input_server
    url2 = "/characters?characterName="
    nickname = input_name
    url3 = "&apikey=IvIirUYlTIIqIHY199xUB0lgOGCVNyY4"

    # 한글 URL을 올바르게 인코딩. 필수 과정.
    url = url1 + server + url2 + quote(nickname) + url3

    # URL 열기
    result = urllib.request.urlopen(url, context=ctx).read()

    info = json.loads(result)
    cha_id = info['rows'][0]['characterId']


    ###################### 서버/닉네임 정보를 통해 받아온 고유 아이디 값으로 모험단 이름 검색하기 [03. 캐릭터 '기본 정보' 조회] #######################

    check_url = "https://api.neople.co.kr/df/servers/" + server + "/characters/" + cha_id + "?apikey=IvIirUYlTIIqIHY199xUB0lgOGCVNyY4"
    check_result = urllib.request.urlopen(check_url, context=ctx).read()
    check_info = json.loads(check_result)
    check_adv = check_info['adventureName']

    if input_adventure == check_adv :
        result = "true"
        return result
        
    else :
        print("캐릭터의 모험단과 입력한 모험단이 일치하지 않습니다.")
        result = "false"
        return result


