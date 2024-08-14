from flask import Flask, request, jsonify
import requests
import json
import pandas as pd


# 출구별 인원
def exitHeadCount_data(date):
    

    url = f"https://apis.openapi.sk.com/puzzle/subway/exit/raw/hourly/stations/133?gender=all&ageGrp=all&date={date}"
    headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "appkey": "qUIhEBWWDd1H4Hn4CiSaF3sVIkJf8acj1l6v4HfN"
    }


    response = requests.get(url, headers=headers) #get 요청 보내기
    contents = response.text #HTTP 응답에서 본문을 추출하여 문자열 형태로 반환
    json_ob = json.loads(contents) # 문자열 형태의 JSON 데이터를 Python 객체로 변환
    raw = json_ob['contents']['raw'] #contents의 raw 내의 데이터만 가져오기

    data = pd.DataFrame(raw)
    return data



# 출구별 인원
def forRawDataExitHeadCount_data(date, time):
    

    url = f"https://apis.openapi.sk.com/puzzle/subway/exit/raw/hourly/stations/133?gender=all&ageGrp=all&date={date}"
    headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "appkey": "qUIhEBWWDd1H4Hn4CiSaF3sVIkJf8acj1l6v4HfN"
    }


    response = requests.get(url, headers=headers) #get 요청 보내기
    contents = response.text #HTTP 응답에서 본문을 추출하여 문자열 형태로 반환
    json_ob = json.loads(contents) # 문자열 형태의 JSON 데이터를 Python 객체로 변환
    raw = json_ob['contents']['raw'] #contents의 raw 내의 데이터만 가져오기

    data = pd.DataFrame(raw) # 데이터프레임 만들기

    year_month_time=f"{date}{time}0000" # 20240702110000 형식으로 변형

    exitData = data[(data['datetime'] == year_month_time)] # 20240702110000 형식으로 변형한 데이터로 날짜와 시간 필터링
    exitData=exitData.drop_duplicates(subset='exit') #중복 제거


    return exitData
