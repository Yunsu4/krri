import pandas as pd
from model.getOffRidersRatio_byCar import getOffRidersRatio_byCar_LineN



def R4_controller(dow, time, R1, cR):

    # 혼잡도 비율 가져오기
    a, b, c, d = (cR[f'{direction} 혼잡도 비율_{line}'].values[0] for direction in ['상행선', '하행선'] for line in [1, 4])


    # 추정된 하차 인원 계산(추정된 하차인원*상하행선 혼잡도 비율)
    R1['추정된 상행선 하차인원_1']= R1['하차인원_1']*a
    R1['추정된 하행선 하차인원_1']= R1['하차인원_1']*b
    R1['추정된 상행선 하차인원_4']= R1['하차인원_4']*c
    R1['추정된 하행선 하차인원_4']= R1['하차인원_4']*d

    R1 = R1.drop(columns=['month', '승차인원_1', '승차인원_4', '하차인원_1', '하차인원_4'], axis=1) # 기존 승차 인원 데이터 삭제


    # 칸별 하차 비율 가져오기
    G1 = getOffRidersRatio_byCar_LineN(dow, int(time), int(1))
    G4 = getOffRidersRatio_byCar_LineN(dow, int(time), int(4))

    G = pd.concat([G1, G4], axis = 0) # 1호선과 4호선 칸별 하차 비율 하나로 합치기
    final_data = calculate_exit_counts(G, R1) # 하차 인원을 계산

    

    return final_data





#-----------------------------------------



# 객차별 하차 인원을 구하는 함수
# 객차별 하차 인원을 계산(추정된 상하행선 하차인원*객차별 하차 비율)
def calculate_exit_counts(G, R):

    exits = R['exit'].unique() # exit 의 값 추출 (중복 제거)

    results = [] # 결과를 담을 리스트 생성

    # G의 모든 platform 열에 있는 각 platform 값을 순회하면서 연산
    for platform in G['platform']:

        # G의 해당 platform과 같은 행에 있는 ratio 값을 ratio에 저장
        ratio = G.loc[G['platform'] == platform, 'ratio'].values[0] 


        # platform 값의 접두사에 따라 column_name을 설정
        if platform.startswith('1-'):
            column_name = '추정된 상행선 하차인원_1'
        elif platform.startswith('2-'):
            column_name = '추정된 하행선 하차인원_1'
        elif platform.startswith('3-'):
            column_name = '추정된 상행선 하차인원_4'
        elif platform.startswith('4-'):
            column_name = '추정된 하행선 하차인원_4'
        else:
            continue  # 해당되지 않는 경우 건너뜀


        # result에 platform 딕셔너리를 추가
        result = {'platform': platform}


        # 모든 exit 열을 순회하면서 해당 출구와 같은 행에 있는 column_name의 값을 가져오고 ratio와 0.01 을 곱해 
        # 객차별 하차 인원을 계산(객차별 하차 비율*추정된 상하행선 하차인원*0.01) (객차별 하차 비율의 경우 % 단위로 나오기 때문에 0.01을 곱하기)
        for exit in exits:
            estimated_value = R.loc[R['exit'] == exit, column_name].values[0]
            result[exit] = ratio * estimated_value*0.01
            
        results.append(result)


    # 리스트를 데이터프레임으로 변환, 기본 인덱스로 변환
    final_result = pd.DataFrame(results)
    final_result.reset_index(drop=True, inplace=True)


    return final_result



