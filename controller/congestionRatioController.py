import pandas as pd
from model.congestionRatio import congestionRatio_data



# 1, 4호선 상하행선 혼잡도 비율을 반환하는 함수
def congestionRatio_controller(dow, time):

    # 혼잡도 비율을 가져오는 함수
    C = congestionRatio_data(dow, time)

    return process_line_data(C) # 정제 후 결과


#----------------------------------------------------------------


#1,4호선 상하행선 혼잡도 비율을 구하는 함수
def process_line_data(C):
    
    # 기존 데이터프레임에서 1, 4호선, 상하행선에 맞추어 값을 선별하고 '상행선 혼잡도_1'과 같이 열을 생성하여 값을 할당
    C.loc[(C['line']==1) & (C['updnLine']==0), '상행선 혼잡도_1'] = C['congestion']
    C.loc[(C['line']==1) & (C['updnLine']==1), '하행선 혼잡도_1'] = C['congestion']
    C.loc[(C['line']==4) & (C['updnLine']==0), '상행선 혼잡도_4'] = C['congestion']
    C.loc[(C['line']==4) & (C['updnLine']==1), '하행선 혼잡도_4'] = C['congestion']

    
    C.fillna(0, inplace=True)# NaN 값을 0으로 대체

    # dow와 hour를 기준으로 그룹화하여 데이터를 집계
    C = C.groupby(['dow', 'hour'], as_index=False).sum()

    # 불필요한 컬럼 제거
    C = C.drop(columns=['line', 'updnLine', 'congestion'])


    # 혼잡도를 이용하여 혼잡도 비율 생성
    C[f'상행선 혼잡도 비율_1'] = (
                C['상행선 혼잡도_1'] / (C['상행선 혼잡도_1'] + C['하행선 혼잡도_1'])
            ).values[0]
    
    C[f'하행선 혼잡도 비율_1'] = (
                C['하행선 혼잡도_1'] / (C['상행선 혼잡도_1'] + C['하행선 혼잡도_1'])
            ).values[0]
    
    C[f'상행선 혼잡도 비율_4'] = (
                C['상행선 혼잡도_4'] / (C['상행선 혼잡도_4'] + C['하행선 혼잡도_4'])
            ).values[0]
    
    C[f'하행선 혼잡도 비율_4'] = (
                C['하행선 혼잡도_4'] / (C['상행선 혼잡도_4'] + C['하행선 혼잡도_4'])
            ).values[0]

    final_data = C.drop(['상행선 혼잡도_1', '하행선 혼잡도_1', '상행선 혼잡도_4', '하행선 혼잡도_4'], axis=1) # 불필요한 컬럼 제거

    

    return final_data

