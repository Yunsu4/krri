import pandas as pd



def R2_controller(R1):

    #R1의 exit 컬럼 가져와서 initial 만들기
    initial = pd.DataFrame({'exit':R1['exit']})


    #상행, 하행 객차별 추정된 승차 인원 구하기
    for i in range(1,11):
        col_name=f'1-{i}'
        initial[col_name] = R1['추정된 승차인원_1']/2/10


    for i in range(1,11):
        col_name=f'2-{i}'
        initial[col_name] = R1['추정된 승차인원_1']/2/10


    for i in range(1,11):
        col_name=f'3-{i}'
        initial[col_name] = R1['추정된 승차인원_4']/2/10


    for i in range(1,11):
        col_name=f'4-{i}'
        initial[col_name] = R1['추정된 승차인원_4']/2/10


    return initial


