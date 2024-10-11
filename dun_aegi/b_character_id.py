import json
import urllib.request, urllib.parse, urllib.error
from urllib.parse import quote
from .config import create_unverified_context
from .a_server_info import get_server_id
from .variable_data import *

def get_character_info(input_adventure, input_server, input_name):
    ctx = create_unverified_context()

    ## 캐릭터 이름 / 서버 로 고유 아이디 값 찾기. 던파 API 가이드 [02. 캐릭터 검색]
    #input_adventure = input("모험단 이름을 입력해주세요. ")
    # 여기에 모험단 이름은 최초로 입력한 값.
    # input_adventure = "난새"
    # input_server = input("서버를 입력해주세요. : ")
    # input_name = input('캐릭터 닉네임을 입력해주세요. : ')

    server = get_server_id(server_list_data, input_server)

    # server 변수에 결과 저장
    if server is not None:
        server_id = server.get('serverId')
    else:
        server_id = None

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
        # 원하는 정보
        # print("고유 캐릭터 넘버 = ", cha_id)  # 실행결과
        # print("캐릭터 이름 = ", info['rows'][0]['characterName'])  # 실행결과
        # print("서버 = ", info['rows'][0]['serverId'])  # 실행결과
        # print("직업 명 = ", info['rows'][0]['jobGrowName'])  # 실행결과
        # print("명성 = ", info['rows'][0]['fame'])  # 실행결과
        character_info = {
            "cha_id": cha_id,
            "character_name": info['rows'][0]['characterName'],
            "server": info['rows'][0]['serverId'],
            "job_root": info['rows'][0]['jobName'],
            "job_name": info['rows'][0]['jobGrowName'],
            "fame": info['rows'][0]['fame']
        }
        return character_info
        
    else :
        print("캐릭터의 모험단과 입력한 모험단이 일치하지 않습니다.")
        return None


