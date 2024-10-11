# 디비 기능 구현부
from .config import db_open, db_close
from .k_db_save import db_save
from .n_nickcheck import chech_nickname

# 디비에 모험단 이름의 테이블 안에 있는 캐릭터들의 uid를 한번에 불러오는 기능.
# sql에서 데이터 꺼내오기.

char_dict = {}
result_list = []  # 결과를 저장할 리스트

def all_update_without_dun(adventure_name):
    conn = None
    cursor = None
    
    try:
        # 데이터베이스 연결 열기
        conn, cursor = db_open()

        if conn is None:            
            raise Exception("데이터베이스 연결을 수립하지 못했습니다.")
        
        # SQL 쿼리 작성
        sql = f"SELECT character_server, character_uid, character_name FROM {adventure_name}"

        # SQL 쿼리 실행
        cursor.execute(sql)

        # 결과 가져오기
        result = cursor.fetchall()

        for row in result:
            server_id = row[0]
            char_id = row[1]
            char_name = row[2]
            # 딕셔너리를 만들어서 리스트에 추가
            character_dict = {"server": server_id, "character_uid": char_id, "character_name": char_name}
            result_list.append(character_dict)

    except Exception as e:
        print(f"Error fetching character_uid from database: {e}")
        result = 'false'
        return result

    finally:
        # 연결 닫기
        db_close(conn, cursor)

    char_dict_result = result_list

    # 리스트를 반복하면서 각 딕셔너리의 서버와 캐릭터 ID 출력
    for character_dict in char_dict_result:
        server_id = character_dict.get("server")
        char_id = character_dict.get("character_uid")
        char_name = character_dict.get("character_name")

        chech_nickname(adventure_name, char_id, char_name)
        db_save(adventure_name, server_id, char_name)
        
        #print(f"서버: {server_id}, 캐릭터 ID: {char_id}, 캐릭터 이름: {char_name}")
    result = 'true'

    return result

# 난새 테이블의 캐릭터 고유 아이디 값 출력
# char_dict_result = character_list("난새")

