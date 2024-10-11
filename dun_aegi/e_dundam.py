from selenium import webdriver
from bs4 import BeautifulSoup
import time


driver = None

def dundam_start():
    global driver
    # Selenium 웹 드라이버 초기화
    driver = webdriver.Chrome()  # Chrome 드라이버를 사용하려면 Chrome이 설치되어 있어야 합니다.


def dundam_finish():
    global driver
    # Selenium 웹 드라이버 초기화
    driver.quit()


def dundam_search(server_id, cha_id):
    global driver
    url = "https://dundam.xyz/character?server=" + server_id + "&key=" + cha_id
    # 서버 정보 + 아이디 고유 ID값 

    # 주어진 URL로 이동
    driver.get(url)

    # 페이지가 로드될 때까지 기다리기 (최대 10초)
    time.sleep(2)

    # 현재 페이지의 소스코드 가져오기
    page_source = driver.page_source

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # name 속성이 "버프계산"인 div 요소 찾기
    buff_calculation_div = soup.find('div', {'name': '버프계산'})

    # 찾은 div 요소의 자식 중 class가 "dval"인 span 태그 찾기
    if buff_calculation_div is None:
        ranking_div = soup.find('div', {'name': '랭킹'})

        if ranking_div: #버프계산 탭이 없을 때, 딜러 탭 추적
            dval_spans = ranking_div.find_all('span', {'class': 'dval'})
            for span in dval_spans:
                print("찾은 span:", span)
                print("span 내용:", span.text)
                target = span.text
                target_class = "deal"
        else :
            print ("버프계산과 랭킹 div를 찾지 못했습니다.")
    else :
        dval_spans = buff_calculation_div.find_all('span', {'class': 'dval'})
        # 첫 번째 dval 클래스를 가진 span 요소의 텍스트 값을 buf에 저장
        target = dval_spans[0].text.replace(',', '') if dval_spans else None
        target_class = "bufer"

    print("원하는 타겟값 :", target, "/ 클래스 :", target_class)

    # 브라우저 닫기
    # driver.quit()

    # 주어진 변수
    number = target

    # 쉼표(,) 제거
    number_targer = float(str(number).replace(',', ''))

    
    # 억으로 출력 (억으로 나누기 10000)
    if target_class == "deal":
        number_int = int(number_targer / 1e8)
        result_target = str(number_int) + "억"
    elif target_class == "bufer":
        number_int = int(number_targer / 1e4)
        result_target = str(number_int) + "만"
    else :
        print("target_class에 오류가 있습니다.")

    return result_target
