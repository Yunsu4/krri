# "sk데이터: 진입 역 기준 칸별 하차 비율"을 csv로 출력하는 파일

from flask import Flask, request, jsonify
import requests
import json
import pandas as pd
from functools import reduce


# sk데이터를 불러오기
def import_data(station_id, dow, time):
    url = f"https://apis.openapi.sk.com/puzzle/subway/congestion/stat/get-off/stations/{station_id}?dow={dow}&hh={time}"
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "appkey": "qUIhEBWWDd1H4Hn4CiSaF3sVIkJf8acj1l6v4HfN"
    }
    
    response = requests.get(url, headers=headers)
    contents = response.text
    json_ob = json.loads(contents)  
    
    return json_ob


# 객차별 하차 비율을 구하는 함수
def get_avg_car_data(json_ob, direction, key_prefix, dow, time):
    
    # ['contents']['stat'] 내 리스트의 첫 번째에 위치한 ['data']에서 getOffCarRate 데이터만 가져오기
    car_data = [stat for stat in json_ob['contents']['stat'] if stat['updnLine'] == direction] 
    if not car_data:
        return pd.DataFrame()
    
    raw_data = car_data[0]['data'] 

    if not raw_data:
        return pd.DataFrame()
        

    # 각 객차의 하차 인원 데이터가 [12, 8, 10, 7, 6, 9, 11, 10, 12, 16] 이와 같이 나오고, 이 데이터는 10분을 주기로 생성된다.
    # n번째 값만 추출하여 평균을 구하면 1시간 기준 n번 객차의 하차 비율을 알 수 있다.
    # 운행 시간대를(05:30 ~ 23:50)로 특정하였기 때문에 6으로 나누지 않고 len(raw_data)로 모든 상황에 대응되는 평균을 구한다.
    averages = [sum(entry['getOffCarRate'][i] for entry in raw_data) / len(raw_data) for i in range(10)]

    # platform 컬럼으 생성하여 n-m 을 데이터로 삽입
    platforms = [f'{key_prefix}-{i+1}' for i in range(10)]

    # 계산한 하차 비율의 평균을 ratio 컬럼의 데이터로 삽입하기 위해 ratios 변수에 저장
    ratios = averages

    
    # 데이터프레임 생성
    car_avg = pd.DataFrame({
        'platform': platforms,
        'ratio': ratios,
        'hour': int(time),
        'dow': dow,
        'line': 1 if key_prefix in ['1','2'] else 4,
        'updnLine': direction
    })

    return car_avg


# 시간대별 객차별 하차 비율을 구하는 함수
def dow_carHeadCount_data(station_id, dow, updnLine, key_prefix):
    
    all_data = [] # 시간대별 데이터를 담을 리스트

    #05시부터 23시까지 시간대별 데이터를 all_data에 저장
    for hour in range(5, 24):
        time = f"{hour:02d}"
        json_ob1 = import_data(station_id, dow, time)
        data = get_avg_car_data(json_ob1, updnLine, key_prefix, dow, time)
        all_data.append(data)
    
    final_data = pd.concat(all_data, ignore_index=True).drop_duplicates() # all_data 리스트 내 데이터를 모두 결합
    final_data = final_data.sort_values(by=['hour']) # hour 기준으로 sort

    
    final_data['updnLine']=updnLine # updnLine 컬럼 추가

    return final_data

# MON~FRI 데이터 동일, SAT~SUN 데이터 동일 하므로 MON, SAT만 구하여 weekday, weekend로 구분
Line1up_weekday = dow_carHeadCount_data(133, 'MON', 0, '1')
Line1up_weekend = dow_carHeadCount_data(133, 'SAT', 0 , '1')
Line1dn_weekday = dow_carHeadCount_data(133, 'MON', 1, '2')
Line1dn_weekend = dow_carHeadCount_data(133, 'SAT', 1, '2')

Line4up_weekday = dow_carHeadCount_data(426, 'MON', 0,'3')
Line4up_weekend = dow_carHeadCount_data(426, 'SAT', 0,'3')
Line4dn_weekday = dow_carHeadCount_data(426, 'MON', 1,'4')
Line4dn_weekend = dow_carHeadCount_data(426, 'SAT', 1,'4')


# 결합할 데이터프레임 리스트
dataframes=[ Line1up_weekday, Line1up_weekend,Line1dn_weekday, Line1dn_weekend,
            Line4up_weekday, Line4up_weekend,Line4dn_weekday, Line4dn_weekend]

# 데이터프레임 결합 (기존 인덱스 무시, 결측값 0으로 표기, 중복값 제거) 
final_data = pd.concat(dataframes, ignore_index=True).fillna(0).drop_duplicates()

# dow컬럼의 MON, SAT 데이터를 weekday, weekend로 변경
final_data['dow'] = final_data['dow'].replace({'MON': 'WEEKDAY', 'SAT': 'WEEKEND'})
                      
final_data.to_csv('sk_getoff_riders_ratio_byCar_toCSV.csv', index=False, encoding='utf-8-sig')