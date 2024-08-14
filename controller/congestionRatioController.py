import datetime
import pandas as pd
from model.congestionRatio import congestionRatio_data_Line1, congestionRatio_data_Line4




def congestionRatio_controller(date, time):

    dow=custom_weekday(date) #날짜를 통해 요일을 구하여 dow에 저장

    json_ob= congestionRatio_data_Line1(dow, time) #1호선 혼잡도 비율(json 형태)
    json_ob4 = congestionRatio_data_Line4(dow, time) #4호선 혼잡도 비율(json 형태)


    merged_1= process_line_data(json_ob,'1') # 1호선 상하행선 혼잡도 비율
    merged_4= process_line_data(json_ob4,'4') # 4호선 상하행선 혼잡도 비율


    R4 = pd.merge(merged_1, merged_4, on=['dow', 'hh', 'mm'], how='outer', suffixes=('', '_drop')).filter(regex='^(?!.*_drop)')


    return R4



#----------------------------------------------------------------

#1,4호선 상하행선 혼잡도 비율을 구하는 함수
def process_line_data(json_ob, line_suffix):
    upData = [stat for stat in json_ob['contents']['stat'] if stat['updnLine']==0] #상행선의 경우 updnLine=0이므로 이를 기반으로 상행선 데이터 추출
    downData = [stat for stat in json_ob['contents']['stat'] if stat['updnLine']==1] #하행선의 경우 updnLine=1이므로 이를 기반으로 하행선 데이터 추출


    #1,4호선 상하행선의 혼잡도를 계산
    #혼잡도의 경우 10분 단위로 데이터를 제공하기 때문에 평균을 1시간의 혼잡도로 정의
    if upData:
        raw= upData[0]['data']
        upLine = pd.DataFrame(raw)
        upLine[f'상행선 혼잡도_{line_suffix}'] = upLine['congestionTrain'].mean() #10분단위로 제공되는 congestionTrain의 평균을 계산
        uL = upLine.drop('congestionTrain', axis=1).drop_duplicates([f'상행선 혼잡도_{line_suffix}']) #congestionTran 열 제거, 상행선 혼잡도의 중복값이 있다면 제거
    else:
        uL= pd.DataFrame()

    if downData:
        raw= downData[0]['data']
        downLine = pd.DataFrame(raw)
        downLine[f'하행선 혼잡도_{line_suffix}'] = downLine['congestionTrain'].mean()
        dL = downLine.drop('congestionTrain', axis=1).drop_duplicates([f'하행선 혼잡도_{line_suffix}'])
    else:
        dL= pd.DataFrame()


    # uL, dL이 다 값이 있다면 상하행선 혼잡도를 이용하여 상하행선 혼잡도 비율을 계산
    if not uL.empty and not dL.empty:
            uL[f'상행선 혼잡도 비율_{line_suffix}'] = (
                uL[f'상행선 혼잡도_{line_suffix}'] / (uL[f'상행선 혼잡도_{line_suffix}'] + dL[f'하행선 혼잡도_{line_suffix}'])
            ).values[0]
            dL[f'하행선 혼잡도 비율_{line_suffix}'] = (
                dL[f'하행선 혼잡도_{line_suffix}'] / (uL[f'상행선 혼잡도_{line_suffix}'] + dL[f'하행선 혼잡도_{line_suffix}'])
            ).values[0]

    
    #uL과 dL을 합쳐 상하행선 혼잡도 비율을 한 데이터프레임에 저장
    return pd.merge(uL, dL, on=['dow', 'hh', 'mm'], how='outer').fillna(0)



#----------------------------------------------------------------

#날짜를 넣으면 요일을 출력해주는 함수
def custom_weekday(input_date):

    #input_date의 경우 20240624와 같은 형태이므로 필요한 부분만 추출하여 연도, 달, 날짜로 구분하여 저장
    year=int(input_date[:4])
    month=int(input_date[4:6])
    day=int(input_date[6:8])


    weekday_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


    #weekday함수를 이용하여 입력한 날의 요일을 추출(숫자로 반환, 월요일=0)
    weekday_int=datetime.date(year,month,day).weekday() 
    weekday= weekday_list[weekday_int] #숫자인 weekday_int를 인덱스로 사용하여 문자열로 요일을 반환


    return weekday