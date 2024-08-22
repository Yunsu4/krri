import boto3
import requests
from io import BytesIO
import re
from datetime import datetime, timedelta



def upload_to_s3(file_obj, bucket_name, s3_filename):
    s3 = boto3.client(
            service_name ="s3",
            region_name= "ap-northeast-2"
        )
    try:
        s3.upload_fileobj(file_obj, bucket_name, s3_filename)
        print(f"File has been uploaded to {bucket_name}/{s3_filename}")
    except Exception as e:
        print(f"Failed to upload file to S3: {e}")



'''
def process_endpoint(url, bucket_name):

    try:
        # 엔드포인트에서 데이터 다운로드 (메모리에서 직접 처리)
        response = requests.get(url, stream=True)
        response.raise_for_status() # 요청 실패시 예외 발생

        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename_match =re.findall('filename="(.+)"', content_disposition)
            if filename_match:
                s3_filename = filename_match[0]
            else:
                raise ValueError("Filename not found in Content-Disposition header")
        else:
            raise ValueError("Content-Disposition header not found in response")
        
        # 데이터가 담긴 스트림을 S3에 직접 업로드
        file_obj = BytesIO(response.content)
        upload_to_s3(file_obj, bucket_name, s3_filename)

    except Exception as e:
        print(f"Error during download or upload: {e}")



def main():
    bucket_name= "odmatrix"


    urls = [
        "http://3.35.146.53:5000/download_estimated-traffic",  # 첫 번째 엔드포인트
        "http://3.35.146.53:5000/download_SK-data"             # 두 번째 엔드포인트 (수정 필요)
    ]


    for url in urls:
        process_endpoint(url, bucket_name)

'''

def process_endpoint(url, bucket_name, default_filename):
    try:
        # 엔드포인트에서 데이터 다운로드 (메모리에서 직접 처리)
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 요청 실패시 예외 발생

        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename_match = re.findall('filename="(.+)"', content_disposition)
            if filename_match:
                s3_filename = filename_match[0]
            else:
                s3_filename = default_filename  
        else:
            s3_filename = default_filename  

        # 데이터가 담긴 스트림을 S3에 직접 업로드
        file_obj = BytesIO(response.content)
        upload_to_s3(file_obj, bucket_name, s3_filename)

    except Exception as e:
        print(f"Error during download or upload: {e}")

def main():
    bucket_name = "odmatrix"

    # default_filename을 웹에서 사용하는 download_name과 동일하게 설정
    urls = [
        ("http://3.35.146.53:5000/download_estimated-traffic", "Day_TrafficData_<date>.zip"),
        ("http://3.35.146.53:5000/download_SK-data", "Day_skData_<date>.zip")
    ]

    for url, default_filename in urls:
        # 날짜를 실제로 대체
        date = (datetime.now() - timedelta(days=29)).strftime("%Y%m%d")
        default_filename = default_filename.replace("<date>", date)

        process_endpoint(url, bucket_name, default_filename)



if __name__ == "__main__":
    main()