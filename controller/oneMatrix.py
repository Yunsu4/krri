import pandas as pd


# -------------- 칸별 승차 인원까지만 구한 하나의 O-D Matrix



# 표에서 R1, R2 부분을 채우기 위해 합치는 함수
def R12_controller(R2):

    # 출발통행이 될 부분을 추가하고 모두 0으로 채우기
    for exitNum in range(1,16):
        col_name=f'{exitNum}'
        R2[col_name] = 0
    
    R2['9-1'] = 0


    return R2



# 표에서 R4, R5 부분을 채우기 위해 합치는 함수
def R45_controller(R4, R5):

    # R4, R5 데이터프레임을 platform 기준으로 합치기
    result = pd.merge(R4, R5, on='platform', how='outer')
    
    # platform 컬럼의 중복이 있다면 없애기
    result = result.loc[:, ~result.columns.duplicated()]


    return result




# 하나의 od Matrix를 반환하는 함수
def oneMatrix_controller(R2, R4, R5):

    # R1, R2, R4, R5를 가져오기
    R12 = R12_controller(R2)
    R45 = R45_controller(R4, R5)



    result = pd.concat([R12, R45], ignore_index = True)  # R1, R2, R4, R5를 합치기

    # R12의 경우 exit, R45의 경우 platform 열을 가지고 있고, 이외에는 모두 동일
    # 하나의 O-D Matrix를 만들기 위해 '출발지/목적지' 열을 만들고 exit, platform 열을 위 아래로 결합
    result['출발지/목적지'] = pd.concat([R12['exit'], R45['platform']], ignore_index = True)
    result = result.drop(columns= ['exit','platform']) # exit, platform 열 삭제
    result = result[['출발지/목적지'] + [col for col in result.columns if col != '출발지/목적지']] # 열 정렬
    


    # 최종적으로 표에 표시될 열 이름
    column_renames = {
        '출발지/목적지': 'M00000', '1': 'E00010', '2': 'E00020', '3': 'E00030', '4': 'E00040', 
        '5': 'E00050', '6': 'E00060', '7': 'E00070', '8': 'E00080', '9': 'E00090', '9-1': 'E00091', 
        '10': 'E00100', '11': 'E00110', '12': 'E00120', '13': 'E00130', '14': 'E00140', '15': 'E00150',
        '1-1': 'T11001', '1-2': 'T11002', '1-3': 'T11003', '1-4': 'T11004', '1-5': 'T11005', 
        '1-6': 'T11006', '1-7': 'T11007', '1-8': 'T11008', '1-9': 'T11009', '1-10': 'T11010',
        '2-1': 'T12001', '2-2': 'T12002', '2-3': 'T12003', '2-4': 'T12004', '2-5': 'T12005',
        '2-6': 'T12006', '2-7': 'T12007', '2-8': 'T12008', '2-9': 'T12009', '2-10': 'T12010',
        '3-1': 'T41001', '3-2': 'T41002', '3-3': 'T41003', '3-4': 'T41004', '3-5': 'T41005',
        '3-6': 'T41006', '3-7': 'T41007', '3-8': 'T41008', '3-9': 'T41009', '3-10': 'T41010',
        '4-1': 'T42001', '4-2': 'T42002', '4-3': 'T42003', '4-4': 'T42004', '4-5': 'T42005',
        '4-6': 'T42006', '4-7': 'T42007', '4-8': 'T42008', '4-9': 'T42009', '4-10': 'T42010'
    }
    
    result = result.rename(columns=column_renames) # column_renames에 기재된대로 열 이름을 수정한다.

    # 원래 '출발지/목적지'였던 'M00000' 열의 데이터도 column_renames의 이름으로 변경 (O-D Matrix의 경우 맨 첫 번째 열과 맨 첫 번째 행이 동일)
    result['M00000'] = result['M00000'].replace(column_renames)


    return result