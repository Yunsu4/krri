import pandas as pd



def R2_controller(R1):


    # R1의 exit 컬럼 가져와서 initial 만들기
    initial = pd.DataFrame({'exit': R1['exit']})
    

    # 각 그룹에 대해 객차별 승차 인원 계산
    승차인원_열 = ['승차인원_1', '승차인원_1', '승차인원_4', '승차인원_4']  # 각 그룹의 승차 인원 열


    for group in range(1, 5):
        for i in range(1, 11):
            col_name = f'{group}-{i}'
            initial[col_name] = R1[승차인원_열[group-1]] / 2 / 10  # 각 객차별로 10으로 나눈 후 2로 나누기



    return initial



