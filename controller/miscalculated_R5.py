'''
import pandas as pd
from model.Line1_4_riders_ratio import Line1_time_preiod_riders_ratio, Line4_time_preiod_riders_ratio, Line1_transfer, Line4_transfer
from model.carHeadCount import carHeadCount_data_Line1, carHeadCount_data_Line4
from controller.R4 import get_avg_car_data
import numpy as np





def R5_controller(cR, date, time):

    dow= cR['dow'].values[0] #요일을 dow 변수에 저장

    

    # Fetch transfer data and check data types
    line4_transfer = Line1_transfer(date) /30
    line1_transfer = Line4_transfer(date) /30
    #print(line1_transfer, line4_transfer)

    print("real sum: ", line1_transfer+line4_transfer)
    


    json_ob = carHeadCount_data_Line1(dow, time) #1호선 객차별 하차 인원 데이터 불러오기
    json_ob4 = carHeadCount_data_Line4(dow, time) #4호선 객차별 하차 인원 데이터 불러오기

    upCar_avg_1 = get_avg_car_data(json_ob, 0, '1', dow, time) # 1호선 상행선 객차별 하차 비율을 구하기
    downCar_avg_1 = get_avg_car_data(json_ob, 1, '2', dow, time) # 1호선 하행선 객차별 하차 비율 구하기
    upCar_avg_4 = get_avg_car_data(json_ob4, 0, '3', dow, time) # 4호선 하행선 객차별 하차 비율 구하기
    downCar_avg_4 = get_avg_car_data(json_ob4, 1, '4', dow, time) # 4호선 하행선 객차별 하차 비율 구하기





    R5=pd.DataFrame() #R5_controller의 결과를 담을 R5 데이터프레임 생성



# 상하행선 혼잡도 비율
    a= cR['상행선 혼잡도 비율_1'].values[0]
    b= cR['하행선 혼잡도 비율_1'].values[0]
    c= cR['상행선 혼잡도 비율_4'].values[0]
    d= cR['하행선 혼잡도 비율_4'].values[0]


    line1 = Line1_time_preiod_riders_ratio(date)
    line4 = Line4_time_preiod_riders_ratio(date)

    a1 = line1[line1['hour'] == time]
    b1 = line4[line4['hour'] == time]

    if a1.empty or b1.empty:
        return 0

    Line1_riders_ratio = a1['탑승 인원 비율'].values[0]
    Line4_riders_ratio = b1['탑승 인원 비율'].values[0]
 



    # 환승 인원 구하기
    # 상하행선의 혼잡도 비율과 각 시간대별 승객 비율의 리스트를 zip으로 묶는다. 
    # 그리고 반복문을 시행한다. start=1로 하여 인덱스가 원래 0이지만 1부터로 변경된다.
    for i, (ratio, car_ratio, rider_ratio) in enumerate(zip([a, b, c, d], [upCar_avg_1, downCar_avg_1, upCar_avg_4, downCar_avg_4],[Line1_riders_ratio, Line1_riders_ratio, Line4_riders_ratio, Line4_riders_ratio]), start=1):
        if i ==1:
            Line1_transfer1 = calculate_transfer_counts(line1_transfer, ratio, car_ratio, rider_ratio,i) # 환승 인원 계산
        elif i ==2:
            Line12_transfer = calculate_transfer_counts(line1_transfer, ratio, car_ratio, rider_ratio,i) # 환승 인원 계산
        elif i ==3:
            Line4_transfer1 = calculate_transfer_counts(line4_transfer, ratio, car_ratio, rider_ratio,i) # 환승 인원 계산
        else:
            Line42_transfer = calculate_transfer_counts(line4_transfer, ratio, car_ratio, rider_ratio,i) # 환승 인원 계산

    R5_1=pd.DataFrame() #R5_controller의 결과를 담을 R5 데이터프레임 생성
    R5_2=pd.DataFrame() #R5_controller의 결과를 담을 R5 데이터프레임 생성

    R5_1 = pd.merge(Line1_transfer1, Line4_transfer1, on=['hour','dow'], how='outer').fillna(0) # 합치기, nall 값은 0으로 채우기
    R5_2 = pd.merge(Line12_transfer, Line42_transfer, on=['hour','dow'], how='outer').fillna(0) # 합치기, nall 값은 0으로 채우기

    R5 = pd.merge(R5_1, R5_2, on=['hour','dow'], how='outer').fillna(0) # 합치기, nall 값은 0으로 채우기
    R5 = R5.drop(columns=['hour','dow'], axis=1)




    #행 열 바꾸고, 인덱스를 리셋하여 platform이라는 컬럼 생성
    R5 = R5.T.reset_index().rename(columns={'index': 'platform'})
    R5.columns=[str(col) if col != 0 else '환승인원' for col in R5.columns] # 원래 index였던 0이 컬럼이 되므로 0 대신 환승인원이라는 컬럼이름을 갖도록 수정



# 모든 시간대의 환승 인원을 더하여 요일 평균과 동일한지 확인할 수 있도록 만든 함수
    #total_sum_for_all_hours = sum_transfer_counts_for_all_hours(cR, date)
    #print(f"Total transfer counts from 05 to 23: {total_sum_for_all_hours}")



    return R5






# 환승인원 계산(환승 인원 * 상하행선 혼잡도 비율 * 객차별 하차 비율)
import pandas as pd
import numpy as np

def calculate_transfer_counts(LineTransfer, ratio, car_ratio, rider_ratio, column_prefix):

    car_ratio = car_ratio.fillna(0)



    updated_transfer = pd.DataFrame()
    #print(f"Function called with column_prefix: {column_prefix}")

    #if column_prefix == 1:
    #    print("1: ", LineTransfer)
    #    print("2: ", ratio)
    #    print("3: ", car_ratio['1-1'])
    #    print("4: ", rider_ratio)
    #else:
    #    print("no~~~")

    for i in range(10):
            col_name = f'{column_prefix}-{i+1}'
            if col_name in car_ratio.columns:
                # Perform the calculation and store the result in the updated_transfer DataFrame
                updated_transfer[col_name] = LineTransfer * ratio * car_ratio[col_name]*rider_ratio*0.01

    # Ensure hour and dow are preserved
    updated_transfer['hour'] = car_ratio['hour']
    updated_transfer['dow'] = car_ratio['dow']

    return updated_transfer


#---------------------------------------------------------------------
def sum_transfer_counts_for_all_hours(cR, date):
    hours_range = [f'{hour:02}' for hour in range(5, 24)]  # '05' to '23'
    total_sum = 0

    for hour in hours_range:
        total_sum += sum_transfer_counts_for_hour(cR, date, hour)
    
    return total_sum




def sum_transfer_counts_for_hour(cR, date, time):

    dow= cR['dow'].values[0] #요일을 dow 변수에 저장

    

    # Fetch transfer data and check data types
    line4_transfer = Line1_transfer(date) /30
    line1_transfer = Line4_transfer(date) /30
    


    json_ob = carHeadCount_data_Line1(dow, time) #1호선 객차별 하차 인원 데이터 불러오기
    json_ob4 = carHeadCount_data_Line4(dow, time) #4호선 객차별 하차 인원 데이터 불러오기

    upCar_avg_1 = get_avg_car_data(json_ob, 0, '1', dow, time) # 1호선 상행선 객차별 하차 비율을 구하기
    downCar_avg_1 = get_avg_car_data(json_ob, 1, '2', dow, time) # 1호선 하행선 객차별 하차 비율 구하기
    upCar_avg_4 = get_avg_car_data(json_ob4, 0, '3', dow, time) # 4호선 하행선 객차별 하차 비율 구하기
    downCar_avg_4 = get_avg_car_data(json_ob4, 1, '4', dow, time) # 4호선 하행선 객차별 하차 비율 구하기





    R5=pd.DataFrame() #R5_controller의 결과를 담을 R5 데이터프레임 생성



# 상하행선 혼잡도 비율
    a= cR['상행선 혼잡도 비율_1'].values[0]
    b= cR['하행선 혼잡도 비율_1'].values[0]
    c= cR['상행선 혼잡도 비율_4'].values[0]
    d= cR['하행선 혼잡도 비율_4'].values[0]


    line1 = Line1_time_preiod_riders_ratio(date)
    line4 = Line4_time_preiod_riders_ratio(date)

    a1 = line1[line1['hour'] == time]
    b1 = line4[line4['hour'] == time]

    if a1.empty or b1.empty:
        return 0

    Line1_riders_ratio = a1['탑승 인원 비율'].values[0]
    Line4_riders_ratio = b1['탑승 인원 비율'].values[0]
 


    total_sum = 0



    # 환승 인원 구하기
    # 상하행선의 혼잡도 비율과 각 시간대별 승객 비율의 리스트를 zip으로 묶는다. 
    # 그리고 반복문을 시행한다. start=1로 하여 인덱스가 원래 0이지만 1부터로 변경된다.
    for i, (ratio, car_ratio, rider_ratio) in enumerate(zip([a, b, c, d], [upCar_avg_1, downCar_avg_1, upCar_avg_4, downCar_avg_4],[Line1_riders_ratio, Line1_riders_ratio, Line4_riders_ratio, Line4_riders_ratio]), start=1):
        if i ==1:
            Line1_transfer1 = calculate_transfer_counts(line1_transfer, ratio, car_ratio, rider_ratio,i) # 환승 인원 계산
        elif i ==2:
            Line12_transfer = calculate_transfer_counts(line1_transfer, ratio, car_ratio, rider_ratio,i) # 환승 인원 계산
        elif i ==3:
            Line4_transfer1 = calculate_transfer_counts(line4_transfer, ratio, car_ratio, rider_ratio,i) # 환승 인원 계산
        else:
            Line42_transfer = calculate_transfer_counts(line4_transfer, ratio, car_ratio, rider_ratio,i) # 환승 인원 계산

    R5_1=pd.DataFrame() #R5_controller의 결과를 담을 R5 데이터프레임 생성
    R5_2=pd.DataFrame() #R5_controller의 결과를 담을 R5 데이터프레임 생성

    R5_1 = pd.merge(Line1_transfer1, Line4_transfer1, on=['hour','dow'], how='outer').fillna(0) # 합치기, nall 값은 0으로 채우기
    R5_2 = pd.merge(Line12_transfer, Line42_transfer, on=['hour','dow'], how='outer').fillna(0) # 합치기, nall 값은 0으로 채우기

    R5 = pd.merge(R5_1, R5_2, on=['hour','dow'], how='outer').fillna(0) # 합치기, nall 값은 0으로 채우기
    R5 = R5.drop(columns=['hour','dow'], axis=1)
    


    for i in range(10):
        
        for j in range(10):
            col_name = f'{i+1}-{j+1}'
            if col_name in R5.columns:
                # Perform the calculation and store the result in the updated_transfer DataFrame
                total_sum += R5[col_name].values[0]
        


    

    return total_sum



'''