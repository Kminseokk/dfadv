import json
import urllib.request, urllib.parse, urllib.error
from urllib.parse import quote
from urllib.error import HTTPError
from .config import *

# 닉네임이 변경된 경우 디비 저장 부분에서 오류가 발생하기에 이 보완하는 코드
def chech_nickname(adventure_name, character_uid, character_name):
    ctx = create_unverified_context()

    try:
        #새롭게 uid를 기준으로 검색하면 그 캐릭터가 닉변했어도 닉변한 이름을 가져옴
        check_url = "https://api.neople.co.kr/df/servers/prey/characters/" + character_uid + "?apikey=IvIirUYlTIIqIHY199xUB0lgOGCVNyY4"
        check_result = urllib.request.urlopen(check_url, context=ctx).read()

        check_info = json.loads(check_result)

        #check_char_uid = check_info['characterId']
        check_char_name = check_info['characterName']

        if check_char_name != character_name:
        # 쿼리 작성 및 실행
            print("닉네임 변경이 확인되어 DB값을 변경합니다.")
            conn, cursor = db_open()
            query = f"SELECT * FROM {adventure_name}"
            cursor.execute(query)

            update_sql = f"UPDATE {adventure_name} SET character_name = %s WHERE character_uid = %s"
            cursor.execute(update_sql, (check_char_name, character_uid))
            conn.commit()  # 커밋
            db_close(conn, cursor)

        else :
            print("닉네임 변경이 확인되지 않았습니다.")

    except HTTPError as e:
        if e.code == 404:
            print("에러 발생. characterId 값을 찾을 수 없습니다.")
            delete_character_row(adventure_name, character_uid)
    

def delete_character_row(adventure_name, character_uid):
    conn, cursor = db_open()
    
    delete_sql = f"DELETE FROM {adventure_name} WHERE character_uid = %s"
    cursor.execute(delete_sql, (character_uid,))
    conn.commit()  # 커밋
    print(f"DELETE 문 확인용 : DELETE FROM {adventure_name} WHERE character_uid = '{character_uid}'")
    
    db_close(conn, cursor)


chech_nickname('난새', '6df73cdf7e181cda6bbee540f568b008', '조태오')