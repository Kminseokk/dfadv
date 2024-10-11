import json
import urllib.request, urllib.parse, urllib.error
from urllib.parse import quote
from .config import create_unverified_context
from datetime import datetime

ctx = create_unverified_context()

def get_dark_land_clear(server_id, cha_id):
    try:
        # 현재 시간을 얻기
        current_time = datetime.now()

        # endDate를 현재 시간으로 설정
        end_date = current_time.strftime("%Y%m%dT%H%M")

        # 최종적으로 startDate와 endDate를 포맷하여 사용
        start_date = "20231108T0000"
        end_date_str = f"{end_date}"

        dark_land_url1 = "https://api.neople.co.kr/df/servers/"
        dark_land_server = server_id + "/characters/"
        dark_land_nickname = cha_id
        dark_land_url2 = f"/timeline?limit=50&code=209&startDate={start_date}&endDate={end_date_str}"
        dark_land_url3 = "&apikey=IvIirUYlTIIqIHY199xUB0lgOGCVNyY4"

        # 한글 URL을 올바르게 인코딩. 필수 과정.
        dark_land_url = dark_land_url1 + dark_land_server + quote(dark_land_nickname) + dark_land_url2 + dark_land_url3

        # URL 열기
        dark_land_result = urllib.request.urlopen(dark_land_url, context=ctx).read()

        dark_land_info = json.loads(dark_land_result)

        choose_region = '어둑섬'

        count_dark_land = sum(1 for entry in dark_land_info['timeline']['rows'] if entry['data']['regionName'] == choose_region)
        #print(f"{choose_region} 의 클리어 횟수는 {count_dark_land} 회 입니다.")

        return count_dark_land

    except urllib.error.URLError as e:
        print(f"URL 열기 오류: {e}")
        return None
    
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

