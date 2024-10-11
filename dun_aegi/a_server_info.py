import json
import urllib.request, urllib.parse, urllib.error
from .config import create_unverified_context
from .variable_data import *

ctx = create_unverified_context()

def get_server_id(data, server_name):
    # 주어진 데이터에서 입력받은 서버 이름에 해당하는 serverId를 찾아 리턴
    # Parameters:
    #     - data (str): JSON 형식의 문자열 데이터
    #     - server_name (str): 찾고자 하는 서버 이름
    # Returns:
    #     - str or None: 찾은 경우 해당 서버의 serverId, 찾지 못한 경우 None
    # 입력된 데이터가 문자열인 경우 딕셔너리로 변환
    if isinstance(data, str):
        try:
            data_dict = json.loads(data)
        except json.JSONDecodeError:
            print("잘못된 JSON 형식입니다.")
            return None
    elif isinstance(data, dict):
        # 이미 딕셔너리인 경우 그대로 사용
        data_dict = data
    else:
        print("잘못된 데이터 유형입니다. JSON 형식의 문자열 또는 딕셔너리여야 합니다.")
        return None

    # 서버 찾기
    for server in data_dict.get('rows', []):
        if server.get('serverName') == server_name:
            return server

    return None
