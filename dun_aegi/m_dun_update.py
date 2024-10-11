# 디비 기능 구현부
from .config import db_open, db_close
from .e_dundam import *
from .n_nickcheck import chech_nickname

# 디비에 모험단 이름의 테이블 안에 있는 캐릭터들의 uid를 한번에 불러오는 기능.
# sql에서 데이터 꺼내오기.

def update_dundam_value(adventure_name):
    conn = None
    cursor = None
    char_dict = {}
    result_list = []  # 결과를 저장할 리스트
    dun_result = None

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
        dun_result = 'false'
        return dun_result

    finally:
        # 연결 닫기
        db_close(conn, cursor)

    char_dict_result = result_list
 
    dundam_start()
    for character_dict in char_dict_result:
        server_id = character_dict.get("server")
        char_id = character_dict.get("character_uid")
        char_name = character_dict.get("character_name")

        chech_nickname(adventure_name, char_id, char_name)

        dundam_value = dundam_search(server_id, char_id)

        # 쿼리 작성 및 실행
        conn, cursor = db_open()
        query = f"SELECT * FROM {adventure_name}"
        cursor.execute(query)

        update_sql = f"UPDATE {adventure_name} SET dungeondeal_val = %s WHERE character_uid = %s"
        cursor.execute(update_sql, (dundam_value, char_id))
        conn.commit()  # 커밋
        db_close(conn, cursor)

        ################### 커밋 종료
        print(f"UPDATE 문 확인용 : {adventure_name} SET dungeondeal_val = {dundam_value} WHERE character_uid = '{char_id}'" )
        
    dundam_finish()
    dun_result = 'true'
    return dun_result
