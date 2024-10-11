from .variable_data import *

data = class_data

# import variable_data

# data = variable_data.class_data

def get_jobGrowId(job_name):
    def recursive_search(rows, target_name):
        for row in rows:
            if row["jobGrowName"] == target_name:
                return row["jobGrowId"]
            if "next" in row:
                result = recursive_search([row["next"]], target_name)
                if result:
                    #print(f"{job_name}의 jobGrowId: {result}")
                    return result
        return None

    for job_class in data["rows"]:
        result_id = recursive_search(job_class["rows"], job_name)
        if result_id:
            #print(f"{job_name}의 jobGrowId: {result_id}")
            return result_id
    return None

#  예제 사용법
# job_name_to_find = "眞 빙결사"
# jobGrowId_result = get_jobGrowId(job_name_to_find)

# if jobGrowId_result:
#     print(f"{job_name_to_find}의 jobGrowId: {jobGrowId_result}")
# else:
#     print(f"{job_name_to_find}을 찾을 수 없습니다.")