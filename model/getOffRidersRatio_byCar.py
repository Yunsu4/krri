import pandas as pd
import os



    # 칸별 하차 비율 데이터(sk_getoff_riders_ratio_byCar_toCSV.py에서 생성한 csv 파일에서 불러온다.)
    # 호선도 입력으로 받아 지정
def getOffRidersRatio_byCar_LineN(dow: str, time: int, line: int) -> pd.DataFrame:
    file_path = 'before_new_odMatrix/sk_getoff_riders_ratio_byCar_toCSV.csv'
    return load_and_filter_data(file_path, dow, time, line)



# 데이터를 불러오고, 필터링하는 함수
def load_and_filter_data(file_path: str, dow: str, time: int, line: int) -> pd.DataFrame:


    # 파일 경로 확인
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    

    # CSV 파일 읽기
    data = pd.read_csv(file_path, encoding='utf-8-sig')
    

    # Dow 변환 (평일은 WEEKDAY, 주말은 WEEKEND로 구분되어 있으므로 이에 맞게 dow를 구분)
    if dow not in ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']:
        raise ValueError("Invalid day of the week. Expected one of ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'].")
    
    dow = 'WEEKDAY' if dow in ['MON', 'TUE', 'WED', 'THU', 'FRI'] else 'WEEKEND'
    

    # 입력 값 검증
    if not isinstance(time, int) or not isinstance(line, int):
        raise ValueError("The time and line parameters must be integers.")
    

    # 필터링 (입력된 요일, 시간, 호선에 맞게 데이터를 필터링)
    filtered_data = data[(data['dow'] == dow) & (data['hour'] == time) & (data['line'] == line)]
    

    return filtered_data







