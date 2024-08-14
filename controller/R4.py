import pandas as pd
from controller import congestionRatioController
from model.carHeadCount import carHeadCount_data_Line1, carHeadCount_data_Line4




def R4_controller(date, time, R1, R4):


    dow=congestionRatioController.custom_weekday(date) #날짜를 통해 요일을 구하여 dow에 저장
    R1['dow']=dow #이후 merge를 하기 위해 dow 컬럼을 추가


    #혼잡도 비율 가져오기
    a, b, c, d = (R4[f'{direction} 혼잡도 비율_{line}'].values[0] for direction in ['상행선', '하행선'] for line in [1, 4])


    #추정된 하차 인원 계산(추정된 하차인원*상하행선 혼잡도 비율)
    R1['추정된 상행선 하차인원_1']= R1['추정된 하차인원_1']*a
    R1['추정된 하행선 하차인원_1']= R1['추정된 하차인원_1']*b
    R1['추정된 상행선 하차인원_4']= R1['추정된 하차인원_4']*c
    R1['추정된 하행선 하차인원_4']= R1['추정된 하차인원_4']*d


    json_ob = carHeadCount_data_Line1(dow, time) #1호선 객차별 하차 인원 데이터 불러오기
    json_ob4 = carHeadCount_data_Line4(dow, time) #4호선 객차별 하차 인원 데이터 불러오기


    # 1호선 상행선
    upCar_avg_1 = get_avg_car_data(json_ob, 0, '1', dow, time) #1호선 객차별 하차 비율을 구하기
    merged_data = pd.merge(upCar_avg_1, R1, on=['hour','dow'], how='outer').fillna(0) # R1과 합치기, nall 값은 0으로 채우기
    merged_data = calculate_exit_counts(merged_data, '1', '추정된 상행선 하차인원_1')


    # 1호선 하행선
    downCar_avg_1 = get_avg_car_data(json_ob, 1, '2', dow, time)
    merged_data = pd.merge(downCar_avg_1, merged_data, on=['hour','dow'], how='outer').fillna(0)
    merged_data = calculate_exit_counts(merged_data, '2', '추정된 하행선 하차인원_1')


    # 4호선 상행선
    upCar_avg_4 = get_avg_car_data(json_ob4, 0, '3', dow, time)
    merged_data = pd.merge(upCar_avg_4, merged_data, on=['hour','dow'], how='outer').fillna(0)
    merged_data = calculate_exit_counts(merged_data, '3', '추정된 상행선 하차인원_4')


    # 4호선 하행선
    downCar_avg_4 = get_avg_car_data(json_ob4, 1, '4', dow, time)
    merged_data = pd.merge(downCar_avg_4, merged_data, on=['hour','dow'], how='outer').fillna(0)
    merged_data = calculate_exit_counts(merged_data, '4', '추정된 하행선 하차인원_4')

    
    # 필요없는 column을 모두 제거
    merged_data = merged_data.drop(columns=['hour', 'dow', '추정된 승차인원_1', '추정된 승차인원_4', '추정된 하차인원_1', '추정된 하차인원_4',
                                             '추정된 상행선 하차인원_1', '추정된 상행선 하차인원_4', '추정된 하행선 하차인원_1', '추정된 하행선 하차인원_4'], axis=1)


    # 행 열 바꾸기
    merged_data.set_index('exit', inplace=True)
    R4_result = merged_data.T
    R4_result.reset_index(inplace=True)
    R4_result.rename(columns={'index':'platform'}, inplace=True)
    

    return R4_result





#-----------------------------------------

#객차별 하차 비율을 구하는 함수
def get_avg_car_data(json_ob, direction, key_prefix, dow, time): 
    car_data = [stat for stat in json_ob['contents']['stat'] if stat['updnLine'] == direction] #json 데이터에서 상하행 구분하여 원하는 데이터만 추출
    if not car_data: #데이터가 비어있다면 빈 데이터프레임 생성
        return pd.DataFrame()
    
    raw_data = car_data[0]['data'] #data만 추출하기(list 중 0번째 값이 data이다)


    #각 객차의 하차 인원 데이터가 [12, 8, 10, 7, 6, 9, 11, 10, 12, 16] 이와 같이 나오고, 이 데이터는 10분을 주기로 생성된다.
    #n번째 값만 추출하여 평균을 구하면 1시간 기준 n번 객차의 혼잡도를 하차 비율을 알 수 있다.
    #운행 시간대를(05:30 ~ 23:50)로 특정하였기 때문에 6으로 나누지 않고 len(raw_data)로 모든 상황에 대응되는 평균을 구한다.
    averages = [sum(entry['getOffCarRate'][i] for entry in raw_data) / len(raw_data) for i in range(10)] 
    car_avg = pd.DataFrame([averages], columns= [f'{key_prefix}-{i+1}' for i in range(10)]) # 위에서 구한 평균을 1-1과 같이 순서대로 넣는다.
   
    #이후 merge를 위해 hour와 dow를 추가한다.
    car_avg['hour'] = time
    car_avg['dow'] = dow

    return car_avg




#-----------------------------------------

#객차별 하차 인원을 구하는 함수
#객차별 상하행선 하차 인원을 계산(추정된 상하행선 하차인원*객차별 하차 비율)
def calculate_exit_counts(merged_data, column_prefix, exit_counts_column):
    for i in range(10):
        col_name=f'{column_prefix}-{i+1}'
        merged_data[col_name] = merged_data[col_name]*merged_data[exit_counts_column]*0.01
    return merged_data