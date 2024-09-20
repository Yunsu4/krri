# 공공데이터 "서울교통공사 역별 일별 시간대별 승하차인원 정보"에서 1년치 자료를 가져온다.
# 이 자료는 1호선의 경우 seoulStation.csv, 4호선의 경우 seoulStation4.csv 로 저장했다고 가정한다.
# read_csv 하는 자료들은 사용하는 자료와 저장된 경로에 맞게 수정하면 된다.

# 공공데이터와 sk 데이터를 이용하여 달, 요일, 시간, 출구별 상하차 인원을 CSV 파일로 만드는 코드

import pandas as pd

# Step 1: SeoulStation{n} 원하는 대로 데이터 처리
def process_seoul_station_data(input_file):
    S1 = pd.read_csv(input_file, encoding='utf-8-sig')

    # '수송일자'를 '날짜' 열로 바꾸고, 데이터 형식도 YYYYMM으로 변경
    S1['수송일자'] = S1['수송일자'].str.replace('2023-', '').str.replace('-', '')
    S1.rename(columns={'수송일자': '날짜'}, inplace=True)
    S1.drop(columns=['호선', '역번호', '역명', '24시이후'], inplace=True) # 필요없는 컬럼 삭제

    # 시간이 포함된 컬럼(05시 이전, 06-07시간대) 이름을 모두 HH로 수정
    new_columns = {}
    for col in S1.columns:
        if '시이전' in col:
            new_columns[col] = '05'
        elif '-' in col:
            new_columns[col] = col.split('-')[0]

        S1.rename(columns=new_columns, inplace=True)


    # 05시 이전, 06-07시간대와 같은 컬럼을 모두 hour 아래의 데이터로 녹이기
    # 원래 05시 이전의 데이터였던 값은 count라는 컬럼을 만들어 그 아래 데이터로 저장
    melted = pd.melt(S1, id_vars=['날짜', '승하차구분'], var_name='hour', value_name='count') 

    # 승하차 구분을 승차, 하차 컬럼으로 각각 구분
    pivoted = melted.pivot_table(index=['날짜', 'hour'], columns='승하차구분', values='count').reset_index()
    pivoted.columns.name = None  # 다중 인덱스로 설정된 열의 이름을 삭제(승하차구분)
    pivoted = pivoted.fillna(0)  # 결측값 0으로 채우기

    return pivoted

# Step 2: 요일별 비율 파일 읽기기
def read_ratios():
    eW = pd.read_csv('exitCount_weekday_ratio.csv', encoding='utf-8-sig')
    eF = pd.read_csv('exitCount_Friday_ratio.csv', encoding='utf-8-sig')
    eSa = pd.read_csv('exitCount_Saturday_ratio.csv', encoding='utf-8-sig')
    eSu = pd.read_csv('exitCount_Sunday_ratio.csv', encoding='utf-8-sig')
    return eW, eF, eSa, eSu

# Step 3: 출구별 인원 계산
def calculate_exit_counts(S1, eW, eF, eSa, eSu):
    
    # 날짜로 요일 구하고 dow에 저장
    S1['날짜'] = S1['날짜'].astype(str)
    S1['날짜_datetime'] = pd.to_datetime('2023' + S1['날짜'], format='%Y%m%d', errors='coerce')
    S1['dow'] = S1['날짜_datetime'].dt.day_name(locale='ko_KR')
    S1.dropna(subset=['날짜_datetime'], inplace=True)
    S1.drop(columns=['날짜_datetime'], inplace=True)

    
    # 시간대별 출구별 승하차 인원 = 승하차인원 * 이용자 비율
    def merge_and_calculate(day_df, ratio_df):
        day_df.loc[:, 'hour'] = day_df['hour'].astype(int)  # hour 열을 int로 변환
        
        merged_df = pd.merge(day_df, ratio_df, on='hour', how='inner')
        merged_df['승차인원'] = merged_df['승차'] * merged_df['userCount_ratio']
        merged_df['하차인원'] = merged_df['하차'] * merged_df['userCount_ratio']
        return merged_df

    # 요일별로 나누어 새로운 데이터 프레임에 저장
    sunday = S1[S1['dow'] == '일요일']
    weekdays = S1[S1['dow'].isin(['월요일', '화요일', '수요일', '목요일'])]
    friday = S1[S1['dow'] == '금요일']
    saturday = S1[S1['dow'] == '토요일']

    # 요일별 시간대별 출구별 승하차 인원
    sunday_merged = merge_and_calculate(sunday, eSu)
    weekdays_merged = merge_and_calculate(weekdays, eW)
    friday_merged = merge_and_calculate(friday, eF)
    saturday_merged = merge_and_calculate(saturday, eSa)

    # 모든 데이터프레임 병합 및 불필요한 컬럼 삭제
    result = pd.concat([weekdays_merged, friday_merged, saturday_merged, sunday_merged], ignore_index=True)
    result.drop(columns=['userCount_ratio', '승차', '하차'], inplace=True)

    
    result['month'] = result['날짜'].str.slice(0, 2)  # 날짜 컬럼에서 MM 추출 후 month로 저장
    # 일별 데이터를 달별로 변환: 같은 달, 요일, 시간, 출구를 가진 데이터의 경우 승하차인원의 평균 계산
    result = result.groupby(['month', 'dow', 'hour', 'exit'], as_index=False).agg({
        '승차인원': 'mean',
        '하차인원': 'mean'
    })

    return result

# 요일 영어로 변경
def convert_day_names(result):
    dow_mapping = {
        '월요일': 'MON',
        '화요일': 'TUE',
        '수요일': 'WED',
        '목요일': 'THU',
        '금요일': 'FRI',
        '토요일': 'SAT',
        '일요일': 'SUN'
    }
    result['dow'] = result['dow'].replace(dow_mapping)
    return result

# 결과를 csv 파일로 저장장
def save_to_csv(result, output_file):
    result.to_csv(output_file, index=False, encoding='utf-8-sig')

# 모든 함수 동작시키는 함수
def process_line_data(line_file, output_file):
    # Process the raw data from Seoul Station
    pivoted_seoul_station = process_seoul_station_data(line_file)
    
    # Read the ratio files
    eW, eF, eSa, eSu = read_ratios()
    
    # Calculate exit counts
    result = calculate_exit_counts(pivoted_seoul_station, eW, eF, eSa, eSu)
    
    # Convert Korean day names to English
    result = convert_day_names(result)
    
    # Save the result to a CSV file
    save_to_csv(result, output_file)
    return result

# 입력 csv 주소
line1_seoul_station_file = 'C:/Users/LG/Desktop/kirri/test/seoulStation.csv'
line4_seoul_station_file = 'C:/Users/LG/Desktop/kirri/test/seoulStation4.csv'

# 출력 csv 주소
line1_output_file = 'Line1_riders.csv'
line4_output_file = 'Line4_riders.csv'

# 모든 함수 동작
result1 = process_line_data(line1_seoul_station_file, line1_output_file)
result4 = process_line_data(line4_seoul_station_file, line4_output_file)
