from .variable_data import *

data = class_data

# import variable_data

# data = variable_data.class_data

def get_job_id(job_name):
    for row in data["rows"]:
        if row["jobName"] == job_name:
            job_id = row["jobId"]
            
            if job_id:
                #print(f"{job_name}의 jobId: {job_id}")
                return job_id
            else:
                #print(f"{job_name}을(를) 찾을 수 없습니다.")    
                return None
    return None

# 함수 호출 예시
# job_name = "귀검사(남)"

# job_id = get_job_id(job_name)


