# 디비 기능 구현부
from .config import db_open, db_close, get_insert_query, create_table

# 기능 구현한 파이썬 파일들 호출
from .b_character_id import get_character_info
from .c_equip import get_item_info
from .d_time_line import get_dark_land_clear
from .f_siv_N_title import get_siv_N_title
from .g_aurora import get_aurora
from .h_Creature import get_creature
from .e_dundam import dundam_search


def db_save(input_adventure, input_server, input_name):
    # 데이터 삽입 SQL 쿼리
    insert_query = get_insert_query(input_adventure)

    try:
        # 캐릭터 정보 가져오기
        result = get_character_info(input_adventure, input_server, input_name)

        if result:
            character_uid = result["cha_id"]
            character_name = result["character_name"]
            character_server = result["server"]
            character_job_root = result["job_root"]
            character_job_name = result["job_name"]
            character_fame = result["fame"]

            conn, cursor = db_open()
            create_table(input_adventure, cursor)
            db_close(conn, cursor)

        else:
            print("main.py 오류 검출. b_.py 에서 캐릭터 검색이 제대로 이루어지지 않음.")
            return "save_false"  # 함수 종료 및 실패 반환

        # 나머지 정보 수집 및 계산
        Custom_epic, mistGear_count, item_level_sum = get_item_info(character_server, character_uid)
        dark_land_conunt = get_dark_land_clear(character_server, character_uid)
        enchant, title = get_siv_N_title(character_server, character_uid)
        fashionista_aurora = get_aurora(character_server, character_uid)
        queen_creature = get_creature(character_server, character_uid)
        dungeondeal_val = "업데이트 필요"  # 던담 딜량 크롤링 부분을 주석 처리하고 임시값으로 설정

        # 데이터 정의
        data = (
            character_uid, input_server, character_name, character_job_root, character_job_name,
            item_level_sum, character_fame, dungeondeal_val, mistGear_count, Custom_epic,
            enchant, queen_creature, fashionista_aurora, title, dark_land_conunt
        )

        # 데이터베이스에 데이터 삽입
        conn, cursor = db_open()

        try:            
            cursor.execute(insert_query, data)
            conn.commit()
        finally:
            db_close(conn, cursor)

        return "save_true"  # 함수 실행 성공시 반환
    
    except Exception as e:
        print(f"오류 발생: {e}")
        return "save_false"  # 함수 실행 실패시 반환
