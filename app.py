from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
from datetime import datetime, timedelta
from controller import R1
from controller import R2
from controller import congestionRatioController
from controller import R4
from controller import R5
from controller import odmatrix_data_processing
from controller import sk_data_processing
from io import BytesIO
from model.Line1_4_riders_ratio import Line1_month_riders_ratio, Line4_month_riders_ratio
from model.exitHeadCount import forRawDataExitHeadCount_data
from model.carHeadCount import forRawData_carHeadCount_Line1, forRawData_carHeadCount_Line4
from model.congestionRatio import forRawData_congestionRatio_Line1, forRawData_congestionRatio_Line4
from controller.congestionRatioController import custom_weekday
import warnings
import subprocess
import zipfile
import upload_csv



# FutureWarning 무시
warnings.simplefilter(action='ignore', category=FutureWarning)


app = Flask(__name__)

# 웹 페이지 첫 화면, 로고 클릭시 표시되는 화면
@app.route('/')
def index():
    return render_template('index.html')


# "estimated traffic DATA" 버튼을 누르면 이동하는 화면
@app.route('/estimated-traffic')
def et():
    return render_template('main.html')


# "About" 버튼을 누르면 이동하는 화면
@app.route('/about')
def about():
    return render_template('about.html')


# "RAW DATA(public)" 버튼을 누르면 이동하는 화면
@app.route('/public-data')
def publicData():
    return render_template('publicData.html')


# "RAW DATA(SK)" 버튼을 누르면 이동하는 화면
@app.route('/SK-data')
def skData():
    return render_template('skData.html')






# "Estimated traffic DATA"에서 submit 버튼을 누르면 이루어지는 로직
# 출발, 도착, 환승 통행 인원을 표시한다.
@app.route('/show_estimated-traffic', methods=['POST'])
def od_matrix():

    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    date = data.get('date')
    time = data.get('time')

    final_R1 = R1.R1_controller(date, time)
    final_R2 = R2.R2_controller(final_R1)
    cR = congestionRatioController.congestionRatio_controller(date, time)
    final_R4 = R4.R4_controller(date, time, final_R1, cR)
    final_R5 = R5.R5_controller(cR, date, time)

    final_R1_result = final_R1.fillna(0).to_dict(orient='records')
    final_R2_result = final_R2.fillna(0).to_dict(orient='records')
    final_R4_result = final_R4.fillna(0).to_dict(orient='records')
    final_R5_result = final_R5.fillna(0).to_dict(orient='records')



    # 리스트 내부의 NaN 값을 처리하는 함수
    def handle_nested_nan(item):
        if isinstance(item, list):
            # 리스트 내부의 NaN 값을 0으로 변환
            return [0 if pd.isna(x) else x for x in item]
        
        elif isinstance(item, pd.Series):
            # Series 내부의 NaN 값을 0으로 변환
            return item.apply(lambda x: 0 if pd.isna(x) else x).tolist()
        
        elif pd.isna(item):
            return 0  # 단일 NaN 값은 0으로 변환
        
        return item  # NaN이 아니면 그대로 반환

    # 데이터프레임을 시리얼라이즈하면서 NaN 처리
    def serialize_df(df):
        df_filled = df.applymap(handle_nested_nan)  # 데이터프레임의 모든 요소에 대해 NaN 처리
        return df_filled.to_dict(orient='records')



    final_R1_result = serialize_df(final_R1)
    final_R2_result = serialize_df(final_R2)
    final_R4_result = serialize_df(final_R4)
    final_R5_result = serialize_df(final_R5)



    return jsonify({
        'final_R1': final_R1_result,
        'final_R2': final_R2_result,
        'final_R4': final_R4_result,
        'final_R5': final_R5_result
    })




# "RAW DATA(public)"에서 submit 버튼을 누르면 이루어지는 로직
# 시간대별 승하차 인원, 요일별 환승 인원을 표시한다.
@app.route('/show_public-data', methods=['POST'])
def show_publicData():

    data = request.get_json()
    date = data.get('date')

    publicData_1= Line1_month_riders_ratio(date)
    publicData_4= Line4_month_riders_ratio(date)

    final_publicData_1 = publicData_1.fillna(0).to_dict(orient='records')
    final_publicData_4 = publicData_4.fillna(0).to_dict(orient='records')

    return jsonify({
            'final_P1': final_publicData_1,
            'final_P4': final_publicData_4
    })



# "RAW DATA(SK)"에서 submit 버튼을 누르면 이루어지는 로직
# 출구별 통행 인원, 1호선 객차별 하차 비율, 4호선 객차별 하차 비율, 1호선 열차 혼잡도, 4호선 열차 혼잡도를 표시한다.
@app.route('/show_SK-data', methods=['POST'])
def show_skData():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')


    dow=custom_weekday(date) #날짜를 통해 요일을 구하여 dow에 저장


    exitData = forRawDataExitHeadCount_data(date, time)
    carHeadCount_1= forRawData_carHeadCount_Line1(dow,time)
    carHeadCount_4= forRawData_carHeadCount_Line4(dow,time)
    congestionRatio_1 =forRawData_congestionRatio_Line1(dow, time)
    congestionRatio_4 =forRawData_congestionRatio_Line4(dow, time)

    final_exitData = exitData.fillna(0).to_dict(orient='records')
    final_carHeadCount_1 = carHeadCount_1.fillna(0).to_dict(orient='records')
    final_carHeadCount_4 = carHeadCount_4.fillna(0).to_dict(orient='records')
    final_congestionRatio_1 = congestionRatio_1.fillna(0).to_dict(orient='records')
    final_congestionRatio_4 = congestionRatio_4.fillna(0).to_dict(orient='records')

    return jsonify({
        'final_exitData': final_exitData,
        'final_carHeadCount_1': final_carHeadCount_1,
        'final_carHeadCount_4': final_carHeadCount_4,
        'final_congestionRatio_1': final_congestionRatio_1,
        'final_congestionRatio_4': final_congestionRatio_4
    })






"""@app.route('/download_estimated-traffic', methods=['GET'])
def download_estimated_traffic():

  # 조회할 수 있는 날짜 중 가장 첫 날을 조회
    current_datetime = datetime.now() # 오늘 날짜와 시간을 datetime 객체로 변환
    new_datetime = current_datetime - timedelta(days=29) # 날짜를 29일 전으로 변경
    date = new_datetime.strftime("%Y%m%d")


    # 최종 zip 파일을 메모리에 생성
    final_zip_buffer = BytesIO()
    with zipfile.ZipFile(final_zip_buffer, 'w', zipfile.ZIP_DEFLATED) as final_zip_file:

        for hour in range(5,24): # 05 ~ 23시까지 time으로 입력
            time = f"{hour:02d}"


            # od_matrix와 동일
            final_R1 = R1.R1_controller(date, time)
            final_R2 = R2.R2_controller(final_R1)
            cR = congestionRatioController.congestionRatio_controller(date, time)
            final_R4 = R4.R4_controller(date, time, final_R1, cR)
            final_R5 = R5.R5_controller(cR, date, time)


            # 각 시간대의 데이터를 처리하여 zip 파일 생성
            time_zip_buffer = odmatrix_data_processing.process_data_and_generate_csvs(final_R1, final_R2, final_R4, final_R5, date, time)

            
            time_zip_filename=f"TrafficData_{date}{time}.zip" # zip 파일 이름 설정
            time_zip_buffer.seek(0) # 각 시간대 zip 파일의 포인터를 맨 처음으로 이동

            # 최종 zip 파일에 각 시간의 zip 파일을 저장
            final_zip_file.writestr(time_zip_filename, time_zip_buffer.read()) 

    # 최종 zip 파일의 포인터를 맨 처음으로 이동
    final_zip_buffer.seek(0)


    # 최종 zip 파일을 "Day_TrafficData_{date}.zip" 이라는 이름으로 반환
    return send_file(
        final_zip_buffer,
        as_attachment=True,
        download_name=f"Day_TrafficData_{date}.zip",
        mimetype='application/zip'
    )"""





"""@app.route('/download_SK-data', methods=['GET'])
def download_skData():

  # 조회할 수 있는 날짜 중 가장 첫 날을 조회
    current_datetime = datetime.now() # 오늘 날짜와 시간을 datetime 객체로 변환
    new_datetime = current_datetime - timedelta(days=29) # 날짜를 29일 전으로 변경
    date = new_datetime.strftime("%Y%m%d")

    dow=custom_weekday(date) #날짜를 통해 요일을 구하여 dow에 저장

    # 최종 zip 파일을 메모리에 생성
    final_zip_buffer = BytesIO()
    with zipfile.ZipFile(final_zip_buffer, 'w', zipfile.ZIP_DEFLATED) as final_zip_file:

        for hour in range(5,24): # 05 ~ 23시까지 time으로 입력
            time = f"{hour:02d}"


            # show_skData와 동일
            exitData = forRawDataExitHeadCount_data(date, time)
            carHeadCount_1= forRawData_carHeadCount_Line1(dow,time)
            carHeadCount_4= forRawData_carHeadCount_Line4(dow,time)
            congestionRatio_1 =forRawData_congestionRatio_Line1(dow, time)
            congestionRatio_4 =forRawData_congestionRatio_Line4(dow, time)


            # 각 시간대의 데이터를 처리하여 zip 파일 생성
            time_zip_buffer = sk_data_processing.process_data_and_generate_csvs(exitData, carHeadCount_1, carHeadCount_4, congestionRatio_1, congestionRatio_4, date, time)

            
            time_zip_filename=f"skData_{date}{time}.zip" # zip 파일 이름 설정
            time_zip_buffer.seek(0) # 각 시간대 zip 파일의 포인터를 맨 처음으로 이동

            # 최종 zip 파일에 각 시간의 zip 파일을 저장
            final_zip_file.writestr(time_zip_filename, time_zip_buffer.read()) 

    # 최종 zip 파일의 포인터를 맨 처음으로 이동
    final_zip_buffer.seek(0)


    # 최종 zip 파일을 "Day_skData_{date}.zip" 이라는 이름으로 반환
    return send_file(
        final_zip_buffer,
        as_attachment=True,
        download_name=f"Day_skData_{date}.zip",
        mimetype='application/zip'
    )"""







@app.route('/download_estimated-traffic', methods=['GET'])
def download_estimated_traffic():
    try:

    # 조회할 수 있는 날짜 중 가장 첫 날을 조회
        current_datetime = datetime.now() # 오늘 날짜와 시간을 datetime 객체로 변환
        new_datetime = current_datetime - timedelta(days=29) # 날짜를 29일 전으로 변경
        date = new_datetime.strftime("%Y%m%d")


        # 최종 zip 파일을 메모리에 생성
        final_zip_buffer = BytesIO()
        with zipfile.ZipFile(final_zip_buffer, 'w', zipfile.ZIP_DEFLATED) as final_zip_file:

            for hour in range(5,24): # 05 ~ 23시까지 time으로 입력
                time = f"{hour:02d}"


                # od_matrix와 동일
                final_R1 = R1.R1_controller(date, time)
                final_R2 = R2.R2_controller(final_R1)
                cR = congestionRatioController.congestionRatio_controller(date, time)
                final_R4 = R4.R4_controller(date, time, final_R1, cR)
                final_R5 = R5.R5_controller(cR, date, time)


                # 각 시간대의 데이터를 처리하여 zip 파일 생성
                time_zip_buffer = odmatrix_data_processing.process_data_and_generate_csvs(final_R1, final_R2, final_R4, final_R5, date, time)

                
                time_zip_filename=f"TrafficData_{date}{time}.zip" # zip 파일 이름 설정
                time_zip_buffer.seek(0) # 각 시간대 zip 파일의 포인터를 맨 처음으로 이동
                final_zip_file.writestr(time_zip_filename, time_zip_buffer.read()) # 최종 zip 파일에 각 시간의 zip 파일을 저장

        # 최종 zip 파일의 포인터를 맨 처음으로 이동
        final_zip_buffer.seek(0)


        bucket_name = "odmatrix"
        s3_filename= f"Day_TrafficData_{date}.zip"
        upload_csv.upload_to_s3(final_zip_buffer, bucket_name, s3_filename)



        # 클라이언트에게 파일 전송
        return jsonify({"message":"sucess"})

    except Exception as e:
        print(f"Error during processing: {e}")
        return jsonify({"error": "Failed to process request"}), 500





@app.route('/download_SK-data', methods=['GET'])
def download_skData():
    try:

    # 조회할 수 있는 날짜 중 가장 첫 날을 조회
        current_datetime = datetime.now() # 오늘 날짜와 시간을 datetime 객체로 변환
        new_datetime = current_datetime - timedelta(days=29) # 날짜를 29일 전으로 변경
        date = new_datetime.strftime("%Y%m%d")

        dow=custom_weekday(date) #날짜를 통해 요일을 구하여 dow에 저장

        # 최종 zip 파일을 메모리에 생성
        final_zip_buffer = BytesIO()
        with zipfile.ZipFile(final_zip_buffer, 'w', zipfile.ZIP_DEFLATED) as final_zip_file:

            for hour in range(5,24): # 05 ~ 23시까지 time으로 입력
                time = f"{hour:02d}"


                # show_skData와 동일
                exitData = forRawDataExitHeadCount_data(date, time)
                carHeadCount_1= forRawData_carHeadCount_Line1(dow,time)
                carHeadCount_4= forRawData_carHeadCount_Line4(dow,time)
                congestionRatio_1 =forRawData_congestionRatio_Line1(dow, time)
                congestionRatio_4 =forRawData_congestionRatio_Line4(dow, time)


                # 각 시간대의 데이터를 처리하여 zip 파일 생성
                time_zip_buffer = sk_data_processing.process_data_and_generate_csvs(exitData, carHeadCount_1, carHeadCount_4, congestionRatio_1, congestionRatio_4, date, time)

                
                time_zip_filename=f"skData_{date}{time}.zip" # zip 파일 이름 설정
                time_zip_buffer.seek(0) # 각 시간대 zip 파일의 포인터를 맨 처음으로 이동
                final_zip_file.writestr(time_zip_filename, time_zip_buffer.read()) # 최종 zip 파일에 각 시간의 zip 파일을 저장

        # 최종 zip 파일의 포인터를 맨 처음으로 이동
        final_zip_buffer.seek(0)

        bucket_name = "odmatrix"
        s3_filename= f"Day_skData_{date}.zip"
        upload_csv.upload_to_s3(final_zip_buffer, bucket_name, s3_filename)



        # 클라이언트에게 파일 전송
        return jsonify({"message":"sucess"})

    except Exception as e:
        print(f"Error during processing: {e}")
        return jsonify({"error": "Failed to process request"}), 500






if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
