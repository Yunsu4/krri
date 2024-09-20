from flask import Flask, request, jsonify, render_template
import pandas as pd
from controller import R1
from controller import R2
from controller import congestionRatioController
from controller import R4
from controller import R5
from controller import oneMatrix_PlusDoor
from model.Line1_4_riders import Line1_riders, Line4_riders
from model.getOffRidersRatio_byCar import getOffRidersRatio_byCar_LineN
from model.congestionRatio import congestionRatio_data_LineN
import warnings



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
    return render_template('estimated_traffic_Data.html')


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
    
    month = data.get('month')
    dow = data.get('dow')
    time = data.get('time')

    final_R1 = R1.R1_controller(month, dow, time)
    final_R2 = R2.R2_controller(final_R1)
    cR = congestionRatioController.congestionRatio_controller(dow, time)
    final_R4 = R4.R4_controller(dow, time, final_R1, cR)
    final_R5 = R5.R5_controller(cR, month, dow, time)
    final_oneMatrix = oneMatrix_PlusDoor.oneMatrix_controller(final_R2, final_R4, final_R5)




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
    final_oneMatrix_result = serialize_df(final_oneMatrix)



    return jsonify({
        'final_R1': final_R1_result,
        'final_R2': final_R2_result,
        'final_R4': final_R4_result,
        'final_R5': final_R5_result,
        'final_oneMatrix': final_oneMatrix_result
    })




# "RAW DATA(public)"에서 submit 버튼을 누르면 이루어지는 로직
# 시간대별 승하차 인원, 요일별 환승 인원을 표시한다.
@app.route('/show_public-data', methods=['POST'])
def show_publicData():

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    month = data.get('month')
    dow = data.get('dow')
    time = data.get('time')

    publicData_1= Line1_riders(month, dow, time)
    publicData_4= Line4_riders(month, dow, time)

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
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    dow = data.get('dow')
    time = data.get('time')



    carHeadCount_1= getOffRidersRatio_byCar_LineN(dow,int(time), int(1))
    carHeadCount_4= getOffRidersRatio_byCar_LineN(dow,int(time), int(4))
    congestionRatio_1 =congestionRatio_data_LineN(dow, int(time), int(1))
    congestionRatio_4 =congestionRatio_data_LineN(dow, int(time), int(4))

    final_carHeadCount_1 = carHeadCount_1.fillna(0).to_dict(orient='records')
    final_carHeadCount_4 = carHeadCount_4.fillna(0).to_dict(orient='records')
    final_congestionRatio_1 = congestionRatio_1.fillna(0).to_dict(orient='records')
    final_congestionRatio_4 = congestionRatio_4.fillna(0).to_dict(orient='records')

    return jsonify({
        'final_carHeadCount_1': final_carHeadCount_1,
        'final_carHeadCount_4': final_carHeadCount_4,
        'final_congestionRatio_1': final_congestionRatio_1,
        'final_congestionRatio_4': final_congestionRatio_4
    })





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
