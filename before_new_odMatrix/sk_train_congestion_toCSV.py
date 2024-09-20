# sk데이터: 진입역 기준 열차 혼잡도 죄종 ver (sk_stasion_congestion_toCSV.py)

from flask import Flask, request, jsonify
import requests
import json
import pandas as pd
from functools import reduce


# sk데이터를 불러오기
def import_data(station_id, dow, time):
    url = f"https://apis.openapi.sk.com/puzzle/subway/congestion/stat/train/stations/{station_id}?dow={dow}&hh={time}"
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "appkey": "qUIhEBWWDd1H4Hn4CiSaF3sVIkJf8acj1l6v4HfN"
    }
    
    response = requests.get(url, headers=headers)
    contents = response.text
    json_ob = response.json()  # JSON 파싱  
    
    return json_ob




# 객차별 혼잡도를 구하는 함수
def get_avg_congestion_data(json_ob, direction, dow, time, station_id):

    car_data = [stat for stat in json_ob['contents']['stat'] if stat['updnLine'] == direction] 
    
    if not car_data or 'data' not in car_data[0] or not car_data[0]['data']:
        return pd.DataFrame()

    
    raw_data = car_data[0]['data'] 
    data = pd.DataFrame(raw_data)
        

    mean_congestion = data['congestionTrain'].mean()
   

    congestion_dataframe = pd.DataFrame({
        'hour': int(time),
        'dow': dow,
        'line': 1 if station_id == 133 else 4,
        'updnLine': direction,
        'congestion':mean_congestion
    }, index=[0])


    return congestion_dataframe


# 시간대별 객차별 혼잡도를 구하는 함수
def dow_congestion_data(station_id, dow, updnLine):
    
    all_data = [] # 시간대별 데이터를 담을 리스트

    #05시부터 23시까지 시간대별 데이터를 all_data에 저장
    for hour in range(5, 24):
        time = f"{hour:02d}"
        json_ob1 = import_data(station_id, dow, time)
        data = get_avg_congestion_data(json_ob1, updnLine, dow, time, station_id)
        all_data.append(data)
    
    final_data = pd.concat(all_data, ignore_index=True).drop_duplicates() # all_data 리스트 내 데이터를 모두 결합
    final_data = final_data.sort_values(by=['hour']) # hour 기준으로 sort    
    final_data['updnLine']=updnLine # updnLine 컬럼 추가

    return final_data



# 모든 호선, 요일, 상하행에 대하여 혼잡도를 구하여 lind_data에 저장
days_of_week = ['MON','TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

line_data = { 'Line1up': [], 'Line1dn': [], 'Line4up': [], 'Line4dn': []}

for day in days_of_week:
    line_data['Line1up'].append(dow_congestion_data(133, day, 0))  # 상행선 (up)
    line_data['Line1dn'].append(dow_congestion_data(133, day, 1))  # 하행선 (dn)
    line_data['Line4up'].append(dow_congestion_data(426, day, 0))  # 상행선 (up)
    line_data['Line4dn'].append(dow_congestion_data(426, day, 1))  # 하행선 (dn)


# Line1 데이터프레임 결합
Line1_dataframes = pd.concat(line_data['Line1up'] + line_data['Line1dn'], ignore_index=True)

# Line4 데이터프레임 결합
Line4_dataframes = pd.concat(line_data['Line4up'] + line_data['Line4dn'], ignore_index=True)


# 데이터프레임 결합 (기존 인덱스 무시, 결측값 0으로 표기, 중복값 제거) 
final_data = pd.concat([Line1_dataframes, Line4_dataframes], ignore_index=True).fillna(0).drop_duplicates()



final_data.to_csv('train_congestion.csv', index=False, encoding='utf-8-sig')

