import pandas as pd


# 1호선 승하차 인원
def Line1_riders(month, dow, time):
    S1 = pd.read_csv('before_new_odMatrix/Line1_riders.csv', encoding='utf-8-sig') # Line1_riders.csv 읽어오기

    seoulStation1 =S1[(S1['month']==int(month)) & (S1['dow']== dow) & (S1['hour']==int(time))] # 입력 값에 해당하는 데이터만 추출

    return seoulStation1
    
    

# 4호선 승하차 인원
def Line4_riders(month, dow, time):
    S1 = pd.read_csv('before_new_odMatrix/Line4_riders.csv', encoding='utf-8-sig') # Line4_riders.csv 읽어오기

    seoulStation4 =S1[(S1['month']==int(month)) & (S1['dow']== dow) & (S1['hour']==int(time))] # 입력 값에 해당하는 데이터만 추출

    return seoulStation4


         









#-------------------------------------------------------------

# 1호선 시간대별 환승인원
def Line1_transfer(month, dow, time):

    S1 = pd.read_csv('before_new_odMatrix/Line1_riders.csv', encoding='utf-8-sig') # S1.csv 읽어오기


    # 서울역, 1호선, 입력된 사용월 자료만 뽑아 seoulStation1
    seoulStation1 =S1[(S1['month']==int(month)) & (S1['dow']== dow)]



    # 요일별 환승 인원
    transfer_counts={
        'SAT': 125109,
        'SUN': 95080,
        'DEFAULT': 144533
    }


    # dow와 매치되는 값이 transfer_counts에 존재하면 그 값에 맞는 counts를 출력하고, 아닌 경우 default 값을 출력
    total_transfer = transfer_counts.get(dow, transfer_counts['DEFAULT'])

 # 시간대별 1호선에서 4호선으로 환승한 인원 계산 (일일 환승 인원* 4호선 승차 인원 비율* 시간대별 탑승 인원 비율)
    Line4_getOn_ratio =Line14_getOn_ratio(month, dow, time)[1] # 4호선 승차 인원 비율을 추출
    Line1_getOn_ratio = total_transfer*Line4_getOn_ratio # 4호선 승차 인원 비율* 일일 환승 인원= 4호선으로 환승한 인원 추출

    
    Line1_time_riders_ratio = calculate_time_period_riders_ratio(seoulStation1) # 탑승 인원 비율을 시간대별로 구한 값
    Line1_time_riders_ratio['환승 인원'] =Line1_time_riders_ratio['탑승 인원 비율']*Line1_getOn_ratio # 시간대별 탑승 인원 비율* 4호선으로 환승한 인원

    #("1호선 환승 인원: ", Line1_time_riders_ratio)


    return Line1_time_riders_ratio




# 4호선 시간대별 환승인원
def Line4_transfer(month, dow, time):

    S1 = pd.read_csv('before_new_odMatrix/Line4_riders.csv', encoding='utf-8-sig') # S1.csv 읽어오기


    # 서울역, 4호선, 입력된 사용월 자료만 뽑아 seoulStation4
    seoulStation4 =S1[(S1['month']==int(month)) & (S1['dow']== dow)]

    #요일별 환승 인원
    transfer_counts={
        'SAT': 125109,
        'SUN': 95080,
        'DEFAULT': 144533
    }


 # 시간대별 4호선에서 1호선으로 환승한 인원 계산 (일일 환승 인원* 1호선 승차 인원 비율* 시간대별 탑승 인원 비율)
    total_transfer = transfer_counts.get(dow, transfer_counts['DEFAULT'])


    Line1_getOn_ratio =Line14_getOn_ratio(month, dow, time)[0] # 1호선 승차 인원 비율을 추출
    Line4_getOn_ratio = total_transfer*Line1_getOn_ratio # 1호선 승차 인원 비율* 일일 환승 인원= 1호선으로 환승한 인원 추출

    Line4_time_riders_ratio = calculate_time_period_riders_ratio(seoulStation4) # 탑승 인원 비율을 시간대별로 구한 값
    Line4_time_riders_ratio['환승 인원'] =Line4_time_riders_ratio['탑승 인원 비율']*Line4_getOn_ratio # 시간대별 탑승 인원 비율* 1호선으로 환승한 인원


    Line4_time_riders_ratio = Line4_time_riders_ratio.fillna(0)

    #("4호선 환승 인원: ", Line4_time_riders_ratio)


    return Line4_time_riders_ratio










#------------------------------------------------------------- 사용된 함수

#시간대별 탑승 인원 비율을 구하는 함수
def calculate_time_period_riders_ratio(seoulStation):


    total_sum = (seoulStation['승차인원'].sum()+seoulStation['하차인원'].sum()) # 05시 부터 24시까지 승하차 인원의 총합



    #시간대를 변수로 다루기 위해 list로 만들기

    columns_time = ['05', '06', '07',
                    '08', '09', '10', '11',
                    '12', '13', '14', '15',
                    '16', '17', '18', '19',
                    '20', '21', '22', '23']

    # 시간대별 탑승 인원 비율을 저장할 데이터프레임 초기화
    time_getOn_ratio = pd.DataFrame(columns=['hour', '탑승 인원 비율'])

    

    # 해당 시간대의 탑승 인원 비율을 계산하여 데이터 프레임에 입력
    for hour in columns_time: #for문을 돌면서 모든 시간대를 입력


        # 같은 시간대의 승차와 하차 인원의 합계를 계산
        time_period_sum = seoulStation[seoulStation['hour'] == int(hour)][['승차인원', '하차인원']].sum().sum()
        time_riders_ratio= (time_period_sum/total_sum) if total_sum != 0 else 0 # 모든 시간대 중 그 해당 시간대의 탑승 인원 추출


        #데이터 프레임에 비율 추가
        time_getOn_ratio=pd.concat([time_getOn_ratio, pd.DataFrame({'hour':[hour], '탑승 인원 비율':[time_riders_ratio]})], ignore_index=True)


    
    return time_getOn_ratio

















# 1,4호선 승차 인원 비율을 구하는 함수 (list 형태로 반환)
def Line14_getOn_ratio(month, dow, time):

    S1 = pd.read_csv('before_new_odMatrix/Line1_riders.csv', encoding='utf-8-sig') # S1.csv 읽어오기
    S4 = pd.read_csv('before_new_odMatrix/Line4_riders.csv', encoding='utf-8-sig') # S1.csv 읽어오기



    # 서울역, 1호선, 입력된 사용월 자료만 추출하여 승차 인원 합계 구하기
    seoulStation1 =S1[(S1['month']==int(month)) & (S1['dow']== dow) & (S1['hour']==int(time))]
    Line1_total_getOn = seoulStation1['승차인원'].sum()


    # 서울역, 4호선, 입력된 사용월 자료만 추출하여 승차 인원 합계 구하기
    seoulStation4 =S4[(S4['month']==int(month)) & (S4['dow']== dow) & (S4['hour']==int(time))]
    Line4_total_getOn = seoulStation4['승차인원'].sum()



    # 서울역 모든 호선의 승차 인원 합계
    total_sum = Line1_total_getOn+Line4_total_getOn
    Line1_getOn_ratio = Line1_total_getOn/(total_sum) # 서울역 모든 호선의 승차 인원 중 1호선 승차 인원의 비율
    Line4_getOn_ratio = Line4_total_getOn/(total_sum) # 서울역 모든 호선의 승차 인원 중 4호선 승차 인원의 비율

    
    Line14_getOn_ratio=[Line1_getOn_ratio, Line4_getOn_ratio] # 1호선 승차 인원 비율, 4호선 승차 인원 비율을 리스트로 반환
    final_Line14_getOn_ratio = [float(x) for x in Line14_getOn_ratio]

    return final_Line14_getOn_ratio



