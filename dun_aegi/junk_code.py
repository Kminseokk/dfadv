
### 03 장비 부분

# 각각 몇개 인가요?
# 주어진 값들을 가지는 딕셔너리 생성
# Custom_epic = {'숲속의 마녀': 0, '블루 베릴': 0, '엔트 정령': 0, '딥 다이버': 0, '블루 파이렛': 0}

# # 딕셔너리 업데이트
# for i in range(0, 13):
#     item_name = item_info['equipment'][i]['itemName']
#     for user_item in Custom_epic.keys():
#         if user_item in item_name:
#             Custom_epic[user_item] += 1

# # 결과 출력
# for user_item, count in Custom_epic.items():
#     print(f"{user_item}의 개수: {count}")


# 06 장비 리스트 순서 알아내기 라인 48
# equipment 리스트에서 slotName 추출
slot_names = [equipment['slotName'] for equipment in item_info['equipment']]

# 결과 출력
print(slot_names)

### 07 아바타 슬롯 리스트 출력하기, 라인 50
# 아바타 리스트 순서 알아내기
# 아바타 리스트에서 slotName 추출
slot_names = [equipment['slotName'] for equipment in avatar_info['avatar']]
print(slot_names)



#a_server_info 코드 36번째 줄부터 삭제한 내용. main으로 이동함

# data_str = variable_data.server_list_data

# # 사용자로부터 서버 이름 입력 받기
# user_input = input("서버 이름을 입력하세요: ")

# # 함수 호출하여 server 정보 얻기
# result = get_server_id(data_str, user_input)

# # 결과 출력
# if result is not None:
#     server_id = result.get('serverId')
#     print(f"{user_input}의 serverId는 {server_id}입니다.")
# else:
#     print(f"{user_input}에 해당하는 서버를 찾을 수 없습니다.")