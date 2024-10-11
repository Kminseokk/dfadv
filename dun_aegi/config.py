# config.py
import ssl
import mysql.connector

def create_unverified_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

# 다음에 사용할 때
# ctx = create_unverified_context()
    
########################################################################################
# 데이터 베이스 사용하기
def db_open():
    # MySQL 서버 연결 정보
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "1234",
        "database": "df_adv",
    }

    # MySQL 연결 생성
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(buffered=True) #. 이 변경 후에 db_open()을 호출한 부분에서는 conn, cursor = db_open()와 같이 사용하면 됨
    return conn, cursor

def db_close(conn, cursor):
    # 연결 종료
    cursor.close()
    conn.close()


########################################################################################
def table_exists(table_name, cursor):
    # 테이블이 존재하는지 확인하는 쿼리
    query = f"SHOW TABLES LIKE '{table_name}';"
    cursor.execute(query)
    return cursor.fetchone() is not None

def create_table(table_name, cursor):
     # 테이블이 이미 존재하는지 확인
    if not table_exists(table_name, cursor):
        # 존재하지 않으면 테이블 생성
        query = f'''
        CREATE TABLE {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            character_uid VARCHAR(255) UNIQUE,
            character_server VARCHAR(255),
            character_name VARCHAR(255),
            character_job_root VARCHAR(255),
            character_job_name VARCHAR(255),
            item_level_sum INT,
            character_fame INT, 
            dungeondeal_val VARCHAR(255),
            mistGear_count INT,
            Custom_epic INT,
            enchant VARCHAR(255),
            queen_creature VARCHAR(255),
            fashionista_aurora VARCHAR(255),
            title VARCHAR(255),
            dark_land_count INT
        );
        '''
        # Execute the query
        cursor.execute(query)

# Example usage:
# conn, cursor = db_open()
# create_table('adventure_name', cursor)
# db_close(conn, cursor)

# Example usage: create_table('adventure_name')
########################################################################################

# 데이터 삽입 SQL 쿼리
def get_insert_query(adv_name):
    # 데이터 삽입 SQL 쿼리
    return f"""
    INSERT INTO {adv_name} (
        character_uid,
        character_server,
        character_name,
        character_job_root,
        character_job_name,
        item_level_sum,
        character_fame,
        dungeondeal_val,
        mistGear_count,
        Custom_epic,
        enchant,
        queen_creature,
        fashionista_aurora,
        title,
        dark_land_count
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    character_server = VALUES(character_server),
    character_name = VALUES(character_name),
    character_job_name = VALUES(character_job_name),
    item_level_sum = VALUES(item_level_sum),
    character_fame = VALUES(character_fame),
    dungeondeal_val = VALUES(dungeondeal_val),
    mistGear_count = VALUES(mistGear_count),
    Custom_epic = VALUES(Custom_epic),
    enchant = VALUES(enchant),
    queen_creature = VALUES(queen_creature),
    fashionista_aurora = VALUES(fashionista_aurora),
    title = VALUES(title),
    dark_land_count = VALUES(dark_land_count)
    """ 

########################################################################################