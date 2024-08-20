from io import StringIO
from zipfile import ZipFile
import io
import pandas as pd

def process_data_and_generate_csvs(exitData, carHeadCount_1, carHeadCount_4, congestionRatio_1, congestionRatio_4, date, time):


    # CSV 파일 생성
    buffer_eD = generate_csv(exitData)
    buffer_cH1 = generate_csv(carHeadCount_1)
    buffer_cH4 = generate_csv(carHeadCount_4)
    buffer_cR1 = generate_csv(congestionRatio_1)
    buffer_cR4 = generate_csv(congestionRatio_4)



    # 파일 이름 생성
    filename_eD = create_filename("ExitData", date, time)
    filename_cH1 = create_filename("Line1_PassengerCount", date, time)
    filename_cH4 = create_filename("Line4_PassengerCount", date, time)
    filename_cR1 = create_filename("Line1_CongestionRatio", date, time)
    filename_cR4 = create_filename("Line4_CongestionRatio", date, time)


    # zip 파일로 압축
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr(filename_eD, buffer_eD.getvalue())
        zip_file.writestr(filename_cH1, buffer_cH1.getvalue())
        zip_file.writestr(filename_cH4, buffer_cH4.getvalue())
        zip_file.writestr(filename_cR1, buffer_cR1.getvalue())
        zip_file.writestr(filename_cR4, buffer_cR4.getvalue())

    zip_buffer.seek(0)

    return zip_buffer




#-------------------------------------------------------------


# CSV 파일로 저장하는 함수
def generate_csv(df):

    for col in df.columns:
        df[col] = df[col].apply(lambda x: x.values[0] if isinstance(x, pd.Series) else x)

    buffer = StringIO()
    df.to_csv(buffer, index=False, encoding='utf-8-sig')
    buffer.seek(0)
    return buffer


# 파일 이름을 만드는 함수
def create_filename(base_name, date, time):
    date_time_suffix = f"{date}{time.replace(':', '')}"  # 시간에 콜론이 있을 경우 제거
    return f"{base_name}_{date_time_suffix}.csv"