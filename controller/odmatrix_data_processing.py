from io import StringIO
from zipfile import ZipFile
import io
import pandas as pd



# 데이터프레임을 받아서 CSV 파일 생성
def process_data_and_generate_csvs(final_R1, final_R2, final_R4, final_R5, date, time):


    # CSV 파일 생성
    buffer_R1 = generate_csv(final_R1)
    buffer_R2 = generate_csv(final_R2)
    buffer_R4 = generate_csv(final_R4)
    buffer_R5 = generate_csv(final_R5)



    # 파일 이름 생성
    filename_R1 = create_filename("PassengerCount", date, time)
    filename_R2 = create_filename("DepartureTraffic", date, time)
    filename_R4 = create_filename("ArrivalTraffic", date, time)
    filename_R5 = create_filename("TransferTraffic", date, time)


    # zip 파일로 압축
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr(filename_R1,buffer_R1.getvalue())
        zip_file.writestr(filename_R2,buffer_R2.getvalue())
        zip_file.writestr(filename_R4,buffer_R4.getvalue())
        zip_file.writestr(filename_R5,buffer_R5.getvalue())

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



