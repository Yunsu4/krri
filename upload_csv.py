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




"""def process_endpoint(url, bucket_name, default_filename):
    try:
        print(f"Downloading from {url}")
        # 엔드포인트에서 데이터 다운로드 (스트리밍 방식으로 직접 처리)
        with requests.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()  # 요청 실패 시 예외 발생
            print("Download completed")

            
            s3_filename = default_filename
            
            print(f"Uploading {s3_filename} to S3")
            # 데이터를 메모리에 저장하지 않고 바로 S3로 스트리밍
            file_obj = BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                file_obj.write(chunk)
            file_obj.seek(0)  # 파일 포인터를 처음으로 이동

            # S3에 업로드
            upload_to_s3(file_obj, bucket_name, s3_filename)
            print(f"Upload completed for {s3_filename}")

    except Exception as e:
        print(f"Error during download or upload: {e}")

def main():
    bucket_name = "odmatrix"

    # default_filename을 웹에서 사용하는 download_name과 동일하게 설정
    urls = [
        ("http://3.35.146.53:5000/download_estimated-traffic", "Day_TrafficData_<date>.zip"),
        ("http://3.35.146.53:5000/download_SK-data", "Day_skData_<date>.zip"),
        ("http://3.35.146.53:5000/download_estimated-traffic1", "Day_TrafficData_<date>.zip")
    ]

    for url, default_filename in urls:
        # 날짜를 실제로 대체
        date = (datetime.now() - timedelta(days=29)).strftime("%Y%m%d")
        default_filename = default_filename.replace("<date>", date)

        process_endpoint(url, bucket_name, default_filename)



if __name__ == "__main__":
    main()"""