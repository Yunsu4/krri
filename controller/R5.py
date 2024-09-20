import pandas as pd
from model.Line1_4_riders import Line1_transfer, Line4_transfer
from model.getOffRidersRatio_byCar import getOffRidersRatio_byCar_LineN




def R5_controller(cR, month, dow, time):

 
    # 1, 4호선 환승 인원 데이터 가져오기
    line1 =Line1_transfer(month, dow, time)
    line4 =Line4_transfer(month, dow, time)


    # 입력된 시간대에 해당하는 환승 인원 추출
    a1 = line1[line1['hour'] == time]
    b1 = line4[line4['hour'] == time]
    

    # 값이 없을 경우 0
    if a1.empty or b1.empty:
        return 0


    # '환승 인원' 열의 데이터만 추출하여 저장
    line1_transfer = a1['환승 인원'].values[0]
    line4_transfer = b1['환승 인원'].values[0]


    # 객차별 하차 비율
    getOffRidersRatio1 = getOffRidersRatio_byCar_LineN(dow, int(time), int(1)) #1호선 객차별 하차 비율 데이터 불러오기
    getOffRidersRatio4 = getOffRidersRatio_byCar_LineN(dow, int(time), int(4)) #4호선 객차별 하차 비율 데이터 불러오기
    getOffRidersRatio = pd.concat([getOffRidersRatio1,getOffRidersRatio4], axis=0) # 1, 4호선 데이터 합치기


    R5=pd.DataFrame() #R5_controller의 결과를 담을 R5 데이터프레임 생성



    # 환승 인원 구하기
    R5 = calculate_transfer_counts(getOffRidersRatio, cR, line1_transfer, line4_transfer)

    R5 = R5.drop(['line', 'updnLine','hour', 'dow'], axis=1)  # 불필요한 열 삭제
    

    # 승강장별로 환승 인원을 나누어 나타내기
    result_data = update_platform_ratios(R5) 

    return result_data






# 환승인원 계산(환승 인원 * 상하행선 혼잡도 비율 * 객차별 하차 비율)

def calculate_transfer_counts(G, cR, line1_transfer, line4_transfer):

    # 상하행선 혼잡도 비율 가져오기
    a = cR['상행선 혼잡도 비율_1'].values[0]
    b = cR['하행선 혼잡도 비율_1'].values[0]
    c = cR['상행선 혼잡도 비율_4'].values[0]
    d = cR['하행선 혼잡도 비율_4'].values[0]

    # G의 각 행을 순회하면서 platform에 따라 ratio 계산
    for index, row in G.iterrows():

        # 각 행의 platform 과 rato 값 추출
        platform = row['platform']
        original_ratio = row['ratio']

        # platform 에 맞는 상하행선 혼잡도 비율을 곱하고 0.01을 곱하기(상하행선 혼잡도 비율의 경우 %단위로 나오므로 0.01을 곱하기)
        if platform.startswith('1-'):
            G.at[index, 'ratio'] = original_ratio * a * line1_transfer * 0.01
        elif platform.startswith('2-'):
            G.at[index, 'ratio'] = original_ratio * b * line1_transfer * 0.01
        elif platform.startswith('3-'):
            G.at[index, 'ratio'] = original_ratio * c * line4_transfer * 0.01
        elif platform.startswith('4-'):
            G.at[index, 'ratio'] = original_ratio * d * line4_transfer * 0.01
        else:
            continue  # 해당되지 않는 경우 건너뜀


    return G



# 승강장별로 나누는 함수 (환승 인원을 상하행, 승강장으로 나누기 위해 20으로 나누고 환승하는 승강장에 맞추어 값을 배정)
def update_platform_ratios(R5):

    # 새로운 열 이름 생성
    new_columns = [f'{i}-{j}' for i in range(1, 5) for j in range(1, 11)]

    # 새로운 열을 0으로 초기화
    for col in new_columns:
        R5[col] = 0

    # R5의 행을 순회하면서 조건에 따라 열 값을 채우기
    for index, row in R5.iterrows():
        platform = row['platform']
        ratio_cal = row['ratio'] / 20  # ratio / 20 계산



    # 1호선의 경우 4호선으로 환승하도록, 4호선의 경우 1호선으로 환승하도록 설정
    # 1, 2로 시작하는 platform은  3, 4로 시작하는  platform 에만 값을 채우기
        if platform.startswith('1') or platform.startswith('2'): 
            # 1-1부터 2-10까지는 0, 3-1부터 4-10까지는 ratio / 20 으로 채우기
            for col in new_columns:
                if col.startswith('1-') or col.startswith('2-'):
                    R5.at[index, col] = 0
                elif col.startswith('3-') or col.startswith('4-'):
                    R5.at[index, col] = ratio_cal


    # 3, 4로 시작하는 platform은  1, 2로 시작하는  platform 에만 값을 채우기
        elif platform.startswith('3') or platform.startswith('4'):
            # 1-1부터 2-10까지는 ratio / 20, 3-1부터 4-10까지는 0 으로 채우기
            for col in new_columns:
                if col.startswith('1-') or col.startswith('2-'):
                    R5.at[index, col] = ratio_cal
                elif col.startswith('3-') or col.startswith('4-'):
                    R5.at[index, col] = 0

    result_data = R5.drop(['ratio'], axis=1)  # 기존 ratio 열 삭제

    
    return result_data






