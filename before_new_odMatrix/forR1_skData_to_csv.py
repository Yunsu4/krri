# to_csv 하는 자료들은 파일명과 저장 경로를 수정

# SK 데이터 시간대별 출구 인원 비율을 CSV 파일로 만드는 코드

# ----------중요-----------
# sk 데이터의 경우 최근 한 달 자료만 제공하므로 날짜 범위 정의(weekdays, Fridays, Saturdays, Sundays) 부분을
# 코딩하는 날짜의 29일 전 기준으로 계산하여 다시 정의해야 한다.


import requests
import pandas as pd
import json
from datetime import datetime, timedelta

# 데이터 가져오기 및 처리
def fetch_and_process_data(start_date, end_date=None):
    url = "https://apis.openapi.sk.com/puzzle/subway/exit/raw/hourly/stations/133?gender=all&ageGrp=all&date={date}"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "appkey": "qUIhEBWWDd1H4Hn4CiSaF3sVIkJf8acj1l6v4HfN"
    }

    all_data = []
    current_date = start_date
    while current_date <= end_date if end_date else start_date:
        date_str = current_date.strftime('%Y%m%d') #날짜를 YYMMDD 형식으로 변환
        formatted_url = url.format(date=date_str) # date에 date_str 을 삽입하여 url 완성

        #데이터 불러오기기
        response = requests.get(formatted_url, headers=headers)
        json_ob = json.loads(response.text)
        raw = json_ob['contents']['raw']
        data = pd.DataFrame(raw)


        pd.set_option('future.no_silent_downcasting', True)
        data = data.fillna(0)
        data['userCount'] = pd.to_numeric(data['userCount'], errors='coerce').fillna(0) # userCount 컬럼을 숫자형으로 변환, 변환 불가한 값은 0
        data['hour'] = data['datetime'].str[8:10] # datetime에서 시간만 HH타입으로 가져오기

        all_data.append(data)

        if end_date: #end_date가 None이 아닌 경우 current_date 하루 증가
            current_date += timedelta(days=1)
    
    final_data = pd.concat(all_data, ignore_index=True) # 데이터프레임 모두 합치기
    final_data = final_data.drop_duplicates() # 중복 제거

    return final_data



# 데이터 비교 및 최종 CSV 파일 생성
def compare_multiple_date_ranges(date_ranges, column_name):
    
    # 모든 날짜 범위의 데이터프레임 리스트로 만들기
    all_data = [fetch_and_process_data(start, end) for start, end in date_ranges] 

    # 각 데이터프레임을 구분하기 위해 range열 추가, 데이터로 range_{n} 사용
    combined_data = pd.concat(all_data, keys=[f'range_{i+1}' for i in range(len(date_ranges))], names=['range']).reset_index()

    # key = exit, hour, range_{n} 가 되고, range_{n}의 데이터가 userCount가 되도록 pivot
    pivot_data = combined_data.pivot_table(index=['exit', 'hour'], columns='range', values='userCount', aggfunc='mean').reset_index()

    # range_{n} 들의 평균을 구하여 새로운 컬럼에 저장 후 range_{n} 컬럼음 삭제
    pivot_data[column_name] = pivot_data[[f'range_{i+1}' for i in range(len(date_ranges))]].mean(axis=1)
    pivot_data = pivot_data.drop(columns=[f'range_{i+1}' for i in range(len(date_ranges))])

    return pivot_data

# 날짜 범위 정의(weekdays, Fridays, Saturdays, Sundays)
weekday_date_ranges = [
    (datetime(2024, 8, 5), datetime(2024, 8, 8)),
    (datetime(2024, 8, 12), datetime(2024, 8, 15)),
    (datetime(2024, 8, 19), datetime(2024, 8, 22)),
    (datetime(2024, 8, 26), datetime(2024, 8, 29))
]

friday_date_ranges = [
    (datetime(2024, 8, 9), datetime(2024, 8, 9)),
    (datetime(2024, 8, 16), datetime(2024, 8, 16)),
    (datetime(2024, 8, 23), datetime(2024, 8, 23)),
    (datetime(2024, 8, 30), datetime(2024, 8, 30))
]

saturday_date_ranges = [
    (datetime(2024, 8, 10), datetime(2024, 8, 10)),
    (datetime(2024, 8, 17), datetime(2024, 8, 17)),
    (datetime(2024, 8, 24), datetime(2024, 8, 24)),
    (datetime(2024, 8, 31), datetime(2024, 8, 31))
]

sunday_date_ranges = [
    (datetime(2024, 8, 4), datetime(2024, 8, 4)),
    (datetime(2024, 8, 11), datetime(2024, 8, 11)),
    (datetime(2024, 8, 18), datetime(2024, 8, 18)),
    (datetime(2024, 8, 25), datetime(2024, 8, 25)),
    (datetime(2024, 9, 1), datetime(2024, 9, 1))
]

# 각 시간대, 출구별 이용자수 평균(weekdays, Fridays, Saturdays, Sundays)
weekday_data = compare_multiple_date_ranges(weekday_date_ranges, 'weekday_userCount')
friday_data = compare_multiple_date_ranges(friday_date_ranges, 'Friday_userCount')
saturday_data = compare_multiple_date_ranges(saturday_date_ranges, 'Saturday_userCount')
sunday_data = compare_multiple_date_ranges(sunday_date_ranges, 'Sunday_userCount')

# 출구별 이용자 비율 (하루 중 그 시간대의 이용자 수 비율)
def calculate_exit_count_ratios(df, column_name):
    df['total_user_count_per_hour'] = df.groupby('hour')[column_name].transform('sum') # column_name을 시간대로 그룹화하여 더하기
    df['userCount_ratio'] = df[column_name] / df['total_user_count_per_hour'] # 동일한 행의 column_name 나누기 total_user_count_per_hour
    df = df.drop(columns=['total_user_count_per_hour', column_name]) # total_user_count_per_hour 컬럼 없애기
    return df

# 최종 출력
def save_ratios_for_day(df, column_name, output_file):
    result = calculate_exit_count_ratios(df, column_name)
    result.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Saved to {output_file}:")
    print(result.head())

# Save ratios for each day
save_ratios_for_day(saturday_data, 'Saturday_userCount', 'exitCount_Saturday_ratio.csv')
save_ratios_for_day(sunday_data, 'Sunday_userCount', 'exitCount_Sunday_ratio.csv')
save_ratios_for_day(friday_data, 'Friday_userCount', 'exitCount_Friday_ratio.csv')
save_ratios_for_day(weekday_data, 'weekday_userCount', 'exitCount_weekday_ratio.csv')
