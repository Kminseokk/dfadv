from flask import Flask, request, render_template, jsonify
import mysql.connector
from dun_aegi.i_class_data import get_job_id
from dun_aegi.j_class_grow import get_jobGrowId
from dun_aegi.b_adv_check import adv_check
from dun_aegi.k_db_save import db_save
from dun_aegi.config import *
from dun_aegi.l_all_update import all_update_without_dun
from dun_aegi.m_dun_update import update_dundam_value
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/rank')
def rank():
    return render_template('wait_page.html')
    # return render_template('rank.html')

@app.route('/data')
def data():
    return render_template('wait_page.html')
    # return render_template('data.html')

# 404 Not Found 오류 핸들링
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_page.html'), 404

@app.route('/properties.html')
def properties():
    image_path = 'image_class/20240111_update_2.webp'

    search_value = request.args.get('search')

    table_name = search_value
    print("테이블 이름 :",table_name)

    conn, cursor = db_open()
    try:
        cursor.execute("SELECT 1")
    except mysql.connector.errors.ProgrammingError:
        
        conn, cursor = db_open()
    
    create_table(table_name, cursor)

    
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    
    try:    
        result = cursor.fetchall()

        # 두 번째 쿼리 실행, 명성가장 높은 캐릭터 
        second_query = f"SELECT * FROM {table_name} ORDER BY character_fame DESC LIMIT 1"
        cursor.execute(second_query)
        repre_char = cursor.fetchall()

        # 세 번째 쿼리 실행, 명성의 합계
        thrid_query = f"SELECT SUM(character_fame) FROM {table_name}"
        cursor.execute(thrid_query)
        fame_sum = cursor.fetchone()[0]  

        # 네 번째 쿼리 실행, 명성의 평균 (버림처리)
        forth_query = f"SELECT ROUND(AVG(character_fame)) FROM {table_name}"
        cursor.execute(forth_query)
        fame_avg = cursor.fetchone()[0]  
        
        # 다섯 번째 쿼리 실행, 어둑섬 클수
        fifth = f"SELECT SUM(dark_land_count) FROM {table_name}"
        cursor.execute(fifth)
        dark_land_sum = cursor.fetchone()[0]  

        # 여섯 번째 쿼리 실행, 미기 수
        sixth = f"SELECT SUM(mistGear_count) FROM {table_name}"
        cursor.execute(sixth)
        mistGear_sum = cursor.fetchone()[0]  

        # 일곱 번째 쿼리 실행, 대표 캐릭터의 직업 이름 꺼내고 이미지 출력과정
        seventh_query = f"SELECT * FROM {table_name} ORDER BY character_fame DESC LIMIT 1"
        cursor.execute(seventh_query)
        class_name = cursor.fetchall()
        
        job_id = get_job_id(class_name[0][4])
        grow_id = get_jobGrowId(class_name[0][5])
        print(job_id, "랑 " , grow_id)
        image_path = f"image_class/{job_id}/{grow_id}.webp"

        
        if os.path.exists(os.path.join(app.static_folder, image_path)):
            print("대표 캐릭터의 값들이 존재하므로 해당 주소의 이미지를 불러옵니다.")
        else:
            
            image_path = 'image_class/20240111_update_2.webp'
            print("대표 캐릭터의 값들이 없으므로 대체 이미지 출력.")
            

    except Exception as e:
        print(f"Error fetching data: {e}")        
        fame_sum = -1
        fame_avg = -1
    
    finally:
        db_close(conn, cursor)

    return render_template('properties.html',
                           search=search_value, result=result, repre_char=repre_char, 
                           fame_sum=fame_sum, fame_avg=fame_avg, dark_land_sum = dark_land_sum,
                           mistGear_sum=mistGear_sum, image_path =image_path )


@app.route('/search', methods=['POST'])
def search():
    # 클라이언트로부터 폼 데이터 받아오기
    server_id = request.form.get('server_id')
    input_name = request.form.get('input_name')
    adventureName = request.form.get('adventureName')

    result = adv_check(adventureName, server_id, input_name) # 결과값은 true false
    print( f" /serach 의 {server_id} 와 {input_name} 의 {adventureName}" )

    # 결과를 클라이언트로 반환
    return result

@app.route('/save', methods=['POST'])
def save():
    # 클라이언트로부터 폼 데이터 받아오기
    server_id = request.form.get('server_id')
    input_name = request.form.get('input_name')
    adventureName = request.form.get('adventureName')

    save_result = db_save(adventureName, server_id, input_name)
    print(f"세이브의 결과 {save_result}")

    # 결과를 클라이언트로 반환
    return save_result

@app.route('/all_update', methods=['POST'])
def all_update():
    data = request.get_json()   

    search_value = data.get('searchValue')
    print(f"Received 업뎃 버튼 search value: {search_value}")
    all_update_result = all_update_without_dun(search_value)

    print("올업데이트 수행", all_update_result)
    # 추가적인 작업 수행 가능
    return all_update_result

@app.route('/dun_update', methods=['POST'])
def dun_update():
    # POST 요청으로 전송된 데이터 받기
    data = request.get_json()

    # 받은 데이터 처리 (여기에서는 간단히 출력만)
    search_value = data.get('searchValue')
    print(f"Received 던담 버튼 search value: {search_value}")
    dun_update_result = update_dundam_value(search_value)

    print(f"던담 업데이트 앱.py 단에서의 확인용 {dun_update_result}")

    # 추가적인 작업 수행 가능
    return dun_update_result


if __name__ == '__main__':
    app.run(debug=True)
