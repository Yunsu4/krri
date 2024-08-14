import pandas as pd
from model.exitHeadCount import exitHeadCount_data
from model.Line1_4_riders_ratio import riders_ratio




def R1_controller(date, time):

    exitData = exitHeadCount_data(date)
    ridersRatio=riders_ratio(date)
    estimated_data = estimate_riders(exitData, ridersRatio) #승하차 인원, 승하차인원 비율 가져와서 추정된 승하차 인원 계산
    result = process_and_sort_data(estimated_data, time) #정렬

    return result



#------------------------------------------------------

#승하차인원 추정 
def estimate_riders(exitData, riders_ratio):


    R1= pd.DataFrame()


#승하차인원 추정 계산

    #exitData, riders_ratio에서 시간만 추출하여 hour 필드를 구성, hour를 기준으로 merge
    exitData['hour']=exitData['datetime'].str[8:10]
    riders_ratio['hour']=riders_ratio['시간대'].str.split('-').str[0].str[:2]
    merged_data = pd.merge(exitData, riders_ratio, on='hour', how='inner')


    #승차 인원 비율과 승차 인원의 곱셈 연산을 통해 1,4호선 승차 인원 열 추가
    R1['추정된 승차인원_1'] = merged_data['userCount'] * merged_data['승차인원 비율_1']
    R1['추정된 승차인원_4'] = merged_data['userCount'] * merged_data['승차인원 비율_4']


    #하차 인원 비율과 하차 인원의 곱셈 연산을 통해 1,4호선 하차 인원 열 추가
    R1['추정된 하차인원_1'] = merged_data['userCount'] * merged_data['하차인원 비율_1']
    R1['추정된 하차인원_4'] = merged_data['userCount'] * merged_data['하차인원 비율_4']


    #R1에 exit, hour 열 추가
    R1['exit'] = merged_data['exit']
    R1['hour'] = merged_data['hour']


    return R1



    

    


#--------------------------------------------

#입력된 시간에 일치하는 데이터만 선별하는 함수
def process_data(R1, time):
    R1 = R1[R1['hour']== time]
    return R1



#9-1을 9 뒤에 정렬하기 위한 함수
def custom_sort(value):
        try:
            return float(value)
        except ValueError:
            return float(value.replace('-', '.'))  # "9-1"을 9.1로 변환
        


#process_data와 custom_sort를 합치는 함수
def process_and_sort_data(R1, time):
     R1= process_data(R1, time)
     R1=R1.drop_duplicates(subset='exit') #중복 제거
     R1=R1.sort_values(by='exit', key=lambda x: x.map(custom_sort))
     return R1

