 #---------------------------------------------혼잡도 비율
import pandas as pd


# N호선 열차 혼잡도 비율
def congestionRatio_data_LineN(dow: str, time: int, line: int) -> pd.DataFrame:
    C1 = pd.read_csv('before_new_odMatrix/train_congestion.csv', encoding='utf-8-sig')

    C1 = C1[(C1['dow'] == dow) & (C1['hour'] == int(time)) & (C1['line'] == line)]

    return C1



# 1, 4호선 열차 혼잡도 비율
def congestionRatio_data(dow: str, time: int) -> pd.DataFrame:
    C1 = pd.read_csv('before_new_odMatrix/train_congestion.csv', encoding='utf-8-sig')

    C1 = C1[(C1['dow'] == dow) & (C1['hour'] == int(time))]

    return C1