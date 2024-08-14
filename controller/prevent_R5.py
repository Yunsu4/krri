
'''
def R5_controller(cR, date, time):


    

    Line1_riders_ratio = Line1_time_preiod_riders_ratio(date)
    Line4_riders_ratio = Line4_time_preiod_riders_ratio(date)

    line1=Line1_riders_ratio[Line1_riders_ratio['hour']==time]
    line2=Line4_riders_ratio[Line4_riders_ratio['hour']==time]


    Line1_riders_ratio= line1['탑승 인원 비율'].values[0]
    Line4_riders_ratio= line2['탑승 인원 비율'].values[0]
    print(Line1_riders_ratio)



    R5=pd.DataFrame() #R5_controller의 결과를 담을 R5 데이터프레임 생성
    dow= cR['dow'].values[0] #요일을 dow 변수에 저장



    a= cR['상행선 혼잡도 비율_1'].values[0]
    b= cR['하행선 혼잡도 비율_1'].values[0]
    c= cR['상행선 혼잡도 비율_4'].values[0]
    d= cR['하행선 혼잡도 비율_4'].values[0]

    sum1= a+b+c+d
    a= a/sum1
    b= b/sum1
    c= c/sum1
    d= d/sum1

    print(a)
    
    transfer_counts={
        'SAT': 125109,
        'SUN': 95080,
        'DEFAULT': 144533
    }


    #dow와 매치되는 값이 transfer_counts에 존재하면 그 값에 맞는 counts를 출력하고, 아닌 경우 default 값을 출력
    total_transfer = transfer_counts.get(dow, transfer_counts['DEFAULT'])  



    # 환승 인원 구하기
    # 상하행선의 혼잡도 비율과 각 시간대별 승객 비율의 리스트를 zip으로 묶는다. 
    # 그리고 반복문을 시행한다. start=1로 하여 인덱스가 원래 0이지만 1부터로 변경된다.
    for i, (ratio, rider_ratio) in enumerate(zip([a, b, c, d], [Line1_riders_ratio, Line1_riders_ratio, Line4_riders_ratio, Line4_riders_ratio]), start=1):
        count = calculate_transfer_counts(ratio, total_transfer, rider_ratio) # 환승 인원 계산
        for j in range(1, 11): # 계산한 환승 인원을 n-1부터 n-10까지에 차례로 저장
            R5.at[0, f'{i}-{j}'] = count



    #행 열 바꾸고, 인덱스를 리셋하여 platform이라는 컬럼 생성
    R5 = R5.T.reset_index().rename(columns={'index': 'platform'})
    R5.columns=[str(col) if col != 0 else '환승인원' for col in R5.columns] # 원래 index였던 0이 컬럼이 되므로 0 대신 환승인원이라는 컬럼이름을 갖도록 수정



# 모든 시간대의 환승 인원을 더하여 요일 평균과 동일한지 확인할 수 있도록 만든 함수
    #total_sum_for_all_hours = sum_transfer_counts_for_all_hours(cR, date)
    #print(f"Total transfer counts from 05 to 23: {total_sum_for_all_hours}")



    return R5



#--------------------------------------------------------------

#환승인원 계산(상하행선 혼잡도 비율*환승 인원*시간대별 환승 인원 비율/10)
def calculate_transfer_counts(ratio, total_transfer,Line_riders_ratio):
    return ratio * total_transfer * Line_riders_ratio / 10 



def sum_transfer_counts_for_all_hours(cR, date):
    hours_range = [f'{hour:02}' for hour in range(5, 24)]  # '05' to '23'
    total_sum = 0

    for hour in hours_range:
        total_sum += sum_transfer_counts_for_hour(cR, date, hour)
    
    return total_sum

def sum_transfer_counts_for_hour(cR, date, time):
    Line1_riders_ratio = Line1_time_preiod_riders_ratio(date)
    Line4_riders_ratio = Line4_time_preiod_riders_ratio(date)

    a = Line1_riders_ratio[Line1_riders_ratio['hour'] == time]
    b = Line4_riders_ratio[Line4_riders_ratio['hour'] == time]

    if a.empty or b.empty:
        return 0

    Line1_riders_ratio = a['탑승 인원 비율'].values[0]
    Line4_riders_ratio = b['탑승 인원 비율'].values[0]

    dow = cR['dow'].values[0]

    a = cR['상행선 혼잡도 비율_1'].values[0]
    b = cR['하행선 혼잡도 비율_1'].values[0]
    c = cR['상행선 혼잡도 비율_4'].values[0]
    d = cR['하행선 혼잡도 비율_4'].values[0]

    sum1= a+b+c+d
    a= a/sum1
    b= b/sum1
    c= c/sum1
    d= d/sum1

    transfer_counts = {
        'SAT': 125109,
        'SUN': 95080,
        'DEFAULT': 144533
    }

    total_transfer = transfer_counts.get(dow, transfer_counts['DEFAULT'])

    total_sum = 0

    for ratio, rider_ratio in zip([a, b, c, d], [Line1_riders_ratio, Line1_riders_ratio, Line4_riders_ratio, Line4_riders_ratio]):
        counts = calculate_transfer_counts(ratio, total_transfer, rider_ratio)
        total_sum += sum(counts)

    return total_sum
'''