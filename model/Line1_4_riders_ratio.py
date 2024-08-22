import pandas as pd



# 1, 4호선 승하차 인원 비율
def riders_ratio(date):

    # S1 = pd.read_csv('C:/Users/LG/Desktop/kirri/OdMatrix_code/S1.csv', encoding='cp949') # S1.csv 읽어오기 절대경로

    S1 = pd.read_csv('S1.csv', encoding='cp949') # S1.csv 읽어오기

    year_month=date[:6] # 연월만 추출



# 서울역, 1호선, 입력된 사용월 자료만 뽑아 seoulStation1
    seoulStation1 =S1[(S1['지하철역']=='서울역') & (S1['호선명']=='1호선') & (S1['사용월']==int(year_month))]
    GetOn1= seoulStation1.filter(regex='승차') #승차 키워드를 포함한 경우 GetOn
    GetOff1= seoulStation1.filter(regex='하차') #하차 키워드를 포함한 경우 GetOff

    dailyGetOn1 = GetOn1/30 #자료는 월합계를 표기하므로 매일의 인원을 파악하기 위해 30으로 나누어 dailyGetOn
    dailyGetOff1 = GetOff1/30 #자료는 월합계를 표기하므로 매일의 인원을 파악하기 위해 30으로 나누어 dailyGetOff



# 서울역, 4호선, 입력된 사용월 자료만 뽑아 seoulStation4
    seoulStation4 =S1[(S1['지하철역']=='서울역') & (S1['호선명']=='4호선')& (S1['사용월']==int(year_month))]
    GetOn4= seoulStation4.filter(regex='승차') #승차 키워드를 포함한 경우 GetOn
    GetOff4= seoulStation4.filter(regex='하차') #하차 키워드를 포함한 경우 GetOff

    dailyGetOn4 = GetOn4/30 #자료는 월합계를 표기하므로 매일의 인원을 파악하기 위해 30으로 나누어 dailyGetOn
    dailyGetOff4 = GetOff4/30 #자료는 월합계를 표기하므로 매일의 인원을 파악하기 위해 30으로 나누어 dailyGetOff

    dailyGetOn1= dailyGetOn1.fillna(0)
    dailyGetOff1= dailyGetOff1.fillna(0)
    dailyGetOn4= dailyGetOn4.fillna(0)
    dailyGetOff4 = dailyGetOff4.fillna(0)


# 1, 4호선 승하차 인원 비율을 계산

    #시간대를 변수로 다루기 위해 list로 만들기
    time_periods = ['05시-06시', '06시-07시', '07시-08시',
                    '08시-09시', '09시-10시', '10시-11시', '11시-12시',
                    '12시-13시', '13시-14시', '14시-15시', '15시-16시',
                    '16시-17시', '17시-18시', '18시-19시', '19시-20시',
                    '20시-21시', '21시-22시', '22시-23시', '23시-24시']


    Line14_rider_ratio = pd.DataFrame() # 승하차 인원 비율을 담을 데이터프레임 생성


    #for문을 돌면서 모든 시간대를 입력
    for time_period in time_periods:
        getOn_col = f'{time_period} 승차인원' 
        getOff_col = f'{time_period} 하차인원'



        # 같은 시간대의 승차와 하차 인원의 비율을 구하여 저장, values[0]으로 실제 값만 추출
        allSum=(dailyGetOn1[getOn_col].values[0]+dailyGetOff1[getOff_col].values[0]+dailyGetOn4[getOn_col].values[0]+dailyGetOff4[getOff_col].values[0])
        
        On_ratio1 = (dailyGetOn1[getOn_col]/allSum)
        Off_ratio1 = (dailyGetOff1[getOff_col]/allSum)
        On_ratio4 = (dailyGetOn4[getOn_col]/allSum)
        Off_ratio4 = (dailyGetOff4[getOff_col]/allSum)

        #데이터 프레임에 비율 추가
        Line14_rider_ratio = pd.concat([Line14_rider_ratio, pd.DataFrame({'시간대': [time_period], '승차인원 비율_1': [On_ratio1], '하차인원 비율_1': [Off_ratio1],'승차인원 비율_4': [On_ratio4], '하차인원 비율_4': [Off_ratio4]})], ignore_index=True)



    return Line14_rider_ratio







#----------------------------------------------------------------------

# 한 달 동안 1호선 승하차 인원 정보(S1 raw data)
def Line1_month_riders_ratio(date):
    S1 = pd.read_csv('S1.csv', encoding='cp949') # S1.csv 읽어오기

    year_month=date[:6] # 연월만 추출

    # 서울역, 1호선, 입력된 사용월 자료만 뽑아 seoulStation1
    seoulStation1 =S1[(S1['지하철역']=='서울역') & (S1['호선명']=='1호선') & (S1['사용월']==int(year_month))]

    return seoulStation1



# 한 달 동안 4호선 승하차 인원 정보(S1 raw data)
def Line4_month_riders_ratio(date):
    S1 = pd.read_csv('S1.csv', encoding='cp949') # S1.csv 읽어오기

    year_month=date[:6] # 연월만 추출

    # 서울역, 4호선, 입력된 사용월 자료만 뽑아 seoulStation4
    seoulStation4 =S1[(S1['지하철역']=='서울역') & (S1['호선명']=='4호선')& (S1['사용월']==int(year_month))]


    return seoulStation4







#-------------------------------------------------------------

# 1호선 시간대별 환승인원
def Line1_transfer(date, dow):

    S1 = pd.read_csv('S1.csv', encoding='cp949') # S1.csv 읽어오기

    year_month=date[:6] # 연월만 추출

    # 서울역, 1호선, 입력된 사용월 자료만 뽑아 seoulStation1
    seoulStation1 = S1[(S1['지하철역'] == '서울역') & (S1['호선명'] == '1호선') & (S1['사용월'] == int(year_month))]



    # 요일별 환승 인원
    transfer_counts={
        'SAT': 125109,
        'SUN': 95080,
        'DEFAULT': 144533
    }

    #print("line1 get on ratio: ", Line14_getOn_ratio(year_month)[0])
    #print("line4 get on ratio: ", Line14_getOn_ratio(year_month)[1])


    # dow와 매치되는 값이 transfer_counts에 존재하면 그 값에 맞는 counts를 출력하고, 아닌 경우 default 값을 출력
    total_transfer = transfer_counts.get(dow, transfer_counts['DEFAULT'])

 # 시간대별 1호선에서 4호선으로 환승한 인원 계산 (일일 환승 인원* 4호선 승차 인원 비율* 시간대별 탑승 인원 비율)
    Line4_getOn_ratio =Line14_getOn_ratio(year_month)[1] # 4호선 승차 인원 비율을 추출
    Line1_getOn_ratio = total_transfer*Line4_getOn_ratio # 4호선 승차 인원 비율* 일일 환승 인원= 4호선으로 환승한 인원 추출
    #print("Line1 transfer: ", Line1_getOn_ratio)
    
    Line1_time_riders_ratio = calculate_time_period_riders_ratio(seoulStation1) # 탑승 인원 비율을 시간대별로 구한 값
    Line1_time_riders_ratio['환승 인원'] =Line1_time_riders_ratio['탑승 인원 비율']*Line1_getOn_ratio # 시간대별 탑승 인원 비율* 4호선으로 환승한 인원

    return Line1_time_riders_ratio




# 4호선 시간대별 환승인원
def Line4_transfer(date, dow):

    S1 = pd.read_csv('S1.csv', encoding='cp949') # S1.csv 읽어오기

    year_month=date[:6] # 연월만 추출

    # 서울역, 4호선, 입력된 사용월 자료만 뽑아 seoulStation4
    seoulStation4 = S1[(S1['지하철역'] == '서울역') & (S1['호선명'] == '4호선') & (S1['사용월'] == int(year_month))]

    #요일별 환승 인원
    transfer_counts={
        'SAT': 125109,
        'SUN': 95080,
        'DEFAULT': 144533
    }


 # 시간대별 4호선에서 1호선으로 환승한 인원 계산 (일일 환승 인원* 1호선 승차 인원 비율* 시간대별 탑승 인원 비율)
    total_transfer = transfer_counts.get(dow, transfer_counts['DEFAULT'])

    Line1_getOn_ratio =Line14_getOn_ratio(year_month)[0] # 1호선 승차 인원 비율을 추출
    Line4_getOn_ratio = total_transfer*Line1_getOn_ratio # 1호선 승차 인원 비율* 일일 환승 인원= 1호선으로 환승한 인원 추출
    #print("Line4 transfer: ", Line4_getOn_ratio)


    Line4_time_riders_ratio = calculate_time_period_riders_ratio(seoulStation4) # 탑승 인원 비율을 시간대별로 구한 값
    Line4_time_riders_ratio['환승 인원'] =Line4_time_riders_ratio['탑승 인원 비율']*Line4_getOn_ratio # 시간대별 탑승 인원 비율* 1호선으로 환승한 인원


    return Line4_time_riders_ratio












#------------------------------------------------------------- 사용된 함수

#시간대별 탑승 인원 비율을 구하는 함수
def calculate_time_period_riders_ratio(seoulStation):

    time_columns = seoulStation.loc[:, '05시-06시 승차인원':'23시-24시 하차인원'].columns #05시 승차인원부터 24시 하차인원까지의 열만 추출
    total_sum = seoulStation[time_columns].sum(axis=1).values[0] # 05시 부터 24시까지 승하차 인원의 총합
    #total_sum_value = seoulStation[time_columns].sum(axis=1) # 05시 부터 24시까지 승하차 인원의 총합


    #시간대를 변수로 다루기 위해 list로 만들기
    time_periods = ['05시-06시', '06시-07시', '07시-08시',
                    '08시-09시', '09시-10시', '10시-11시', '11시-12시',
                    '12시-13시', '13시-14시', '14시-15시', '15시-16시',
                    '16시-17시', '17시-18시', '18시-19시', '19시-20시',
                    '20시-21시', '21시-22시', '22시-23시', '23시-24시']

    columns_time = ['05', '06', '07',
                    '08', '09', '10', '11',
                    '12', '13', '14', '15',
                    '16', '17', '18', '19',
                    '20', '21', '22', '23']

    time_getOn_ratio= pd.DataFrame()


    # 해당 시간대의 탑승 인원 비율을 계산하여 데이터 프레임에 입력
    for idx, time_period in enumerate(time_periods): #for문을 돌면서 모든 시간대를 입력
        getOn_col = f'{time_period} 승차인원' 
        getOff_col = f'{time_period} 하차인원'


        # 같은 시간대의 승차와 하차 인원의 비율을 구하여 저장, values[0]으로 실제 값만 추출
        time_period_sum=(seoulStation[getOn_col].values[0]+seoulStation[getOff_col].values[0])
        time_period_sum=(seoulStation[getOn_col]+seoulStation[getOff_col]).values[0]
        

        time_riders_ratio= (time_period_sum/total_sum) if total_sum != 0 else 0 # 모든 시간대 중 그 해당 시간대의 탑승 인원 추출


        #데이터 프레임에 비율 추가
        time_getOn_ratio=pd.concat([time_getOn_ratio, pd.DataFrame({'hour':[columns_time[idx]], '탑승 인원 비율':[time_riders_ratio]})], ignore_index=True)


    return time_getOn_ratio

















# 1,4호선 승차 인원 비율을 구하는 함수 (list 형태로 반환)
def Line14_getOn_ratio(year_month):

    S1 = pd.read_csv('S1.csv', encoding='cp949') # S1.csv 읽어오기



    # 서울역, 1호선, 입력된 사용월 자료만 추출하여 승차 인원 합계 구하기
    seoulStation1 = S1[(S1['지하철역'] == '서울역') & (S1['호선명'] == '1호선') & (S1['사용월'] == int(year_month))]
    Line1_total_getOn = calculate_total_riders(seoulStation1)


    # 서울역, 4호선, 입력된 사용월 자료만 추출하여 승차 인원 합계 구하기
    seoulStation4 = S1[(S1['지하철역'] == '서울역') & (S1['호선명'] == '4호선') & (S1['사용월'] == int(year_month))]
    Line4_total_getOn = calculate_total_riders(seoulStation4)


    # 서울역, 경의선, 입력된 사용월 자료만 추출하여 승차 인원 합계 구하기
    seoulStationK = S1[(S1['지하철역'] == '서울역') & (S1['호선명'] == '경의선') & (S1['사용월'] == int(year_month))]
    LineK_total_getOn = calculate_total_riders(seoulStationK)


    # 서울역, 공항철도 1호선, 입력된 사용월 자료만 추출하여 승차 인원 합계 구하기
    seoulStationP = S1[(S1['지하철역'] == '서울역') & (S1['호선명'] == '공항철도 1호선') & (S1['사용월'] == int(year_month))]
    LineP_total_getOn = calculate_total_riders(seoulStationP)


    # 서울역 모든 호선의 승차 인원 합계
    total_sum = Line1_total_getOn+Line4_total_getOn+LineP_total_getOn+LineK_total_getOn

    Line1_getOn_ratio = Line1_total_getOn/(total_sum) # 서울역 모든 호선의 승차 인원 중 1호선 승차 인원의 비율
    Line4_getOn_ratio = Line4_total_getOn/(total_sum) # 서울역 모든 호선의 승차 인원 중 4호선 승차 인원의 비율

    
    Line14_getOn_ratio=[Line1_getOn_ratio, Line4_getOn_ratio] # 1호선 승차 인원 비율, 4호선 승차 인원 비율을 리스트로 반환
    final_Line14_getOn_ratio = [float(x) for x in Line14_getOn_ratio]

    #print("final Line14_getOn_ratio: ", final_Line14_getOn_ratio)
    return final_Line14_getOn_ratio



# 05시~24시까지 승차인원의 합계를 구하는 함수
def calculate_total_riders(seoulStation):
    

    #시간대를 변수로 다루기 위해 list로 만들기
    time_periods = ['05시-06시', '06시-07시', '07시-08시',
                    '08시-09시', '09시-10시', '10시-11시', '11시-12시',
                    '12시-13시', '13시-14시', '14시-15시', '15시-16시',
                    '16시-17시', '17시-18시', '18시-19시', '19시-20시',
                    '20시-21시', '21시-22시', '22시-23시', '23시-24시']


 # 지정한 시간대의 모든 승차 인원을 더하기
    total_getOn = 0
    for time_period in time_periods:
        getOn_col = f'{time_period} 승차인원'
        total_getOn += seoulStation[getOn_col].values[0]

    return total_getOn



