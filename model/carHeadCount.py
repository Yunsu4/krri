from flask import Flask, request, jsonify
import requests
import json
import pandas as pd



# 객차별 하차 인원

# 1호선
def carHeadCount_data_Line1(dow, time):

    url = f"https://apis.openapi.sk.com/puzzle/subway/congestion/stat/get-off/stations/133?dow={dow}&hh={time}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "appkey": "qUIhEBWWDd1H4Hn4CiSaF3sVIkJf8acj1l6v4HfN"
    }


    response = requests.get(url, headers=headers) #get 요청 보내기
    contents = response.text #HTTP 응답에서 본문을 추출하여 문자열 형태로 반환
    json_ob = json.loads(contents) # 문자열 형태의 JSON 데이터를 Python 객체로 변환


    return json_ob



# 4호선
def carHeadCount_data_Line4(dow, time):

    url = f"https://apis.openapi.sk.com/puzzle/subway/congestion/stat/get-off/stations/426?dow={dow}&hh={time}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "appkey": "qUIhEBWWDd1H4Hn4CiSaF3sVIkJf8acj1l6v4HfN"
    }


    response = requests.get(url, headers=headers) #get 요청 보내기
    contents = response.text #HTTP 응답에서 본문을 추출하여 문자열 형태로 반환
    json_ob = json.loads(contents) # 문자열 형태의 JSON 데이터를 Python 객체로 변환

    return json_ob







#------------------------------------------------------------------
# 1호선 객차별 하차 인원


def forRawData_carHeadCount_Line1(dow, time):

    url = f"https://apis.openapi.sk.com/puzzle/subway/congestion/stat/get-off/stations/133?dow={dow}&hh={time}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "appkey": "qUIhEBWWDd1H4Hn4CiSaF3sVIkJf8acj1l6v4HfN"
    }


    response = requests.get(url, headers=headers) #get 요청 보내기
    contents = response.text #HTTP 응답에서 본문을 추출하여 문자열 형태로 반환
    json_ob = json.loads(contents) # 문자열 형태의 JSON 데이터를 Python 객체로 변환

    upcar_data = [stat for stat in json_ob['contents']['stat'] if stat['updnLine'] == 0] # 상행 데이터만 추출
    if not upcar_data: #데이터가 비어있다면 빈 데이터프레임 생성
        return pd.DataFrame()
    
    upLine_data = upcar_data[0]['data'] #data만 추출하기(list 중 0번째 값이 data이다)
    upLine = pd.DataFrame(upLine_data)



    downcar_data = [stat for stat in json_ob['contents']['stat'] if stat['updnLine'] == 1] # 하행 데이터만 추출
    if not downcar_data: #데이터가 비어있다면 빈 데이터프레임 생성
        return pd.DataFrame()
    
    downLine_data = downcar_data[0]['data'] #data만 추출하기(list 중 0번째 값이 data이다)
    downLine = pd.DataFrame(downLine_data)

    merged_data = pd.merge(upLine, downLine, on=['hh','dow','mm'], how='outer').fillna(0) # 상하행 데이터를 합치기, null 값은 0으로 채우기


    return merged_data



# 4호선 객차별 하차 인원
def forRawData_carHeadCount_Line4(dow, time):

    url = f"https://apis.openapi.sk.com/puzzle/subway/congestion/stat/get-off/stations/426?dow={dow}&hh={time}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "appkey": "qUIhEBWWDd1H4Hn4CiSaF3sVIkJf8acj1l6v4HfN"
    }


    response = requests.get(url, headers=headers) #get 요청 보내기
    contents = response.text #HTTP 응답에서 본문을 추출하여 문자열 형태로 반환
    json_ob = json.loads(contents) # 문자열 형태의 JSON 데이터를 Python 객체로 변환


    upcar_data = [stat for stat in json_ob['contents']['stat'] if stat['updnLine'] == 0] # 상행 데이터만 추출
    if not upcar_data: #데이터가 비어있다면 빈 데이터프레임 생성
        return pd.DataFrame()
    
    upLine_data = upcar_data[0]['data'] #data만 추출하기(list 중 0번째 값이 data이다)
    upLine = pd.DataFrame(upLine_data)



    downcar_data = [stat for stat in json_ob['contents']['stat'] if stat['updnLine'] == 1] # 하행 데이터만 추출
    if not downcar_data: #데이터가 비어있다면 빈 데이터프레임 생성
        return pd.DataFrame()
    
    downLine_data = downcar_data[0]['data'] #data만 추출하기(list 중 0번째 값이 data이다)
    downLine = pd.DataFrame(downLine_data)

    merged_data = pd.merge(upLine, downLine, on=['hh','dow','mm'], how='outer').fillna(0) # 상하행 데이터를 합치기, null 값은 0으로 채우기


    return merged_data

