import boto3


def s3_connection():
    try: 
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name ="s3",
            region_name= "ap-northeast-2",
            aws_access_key_id="AKIAQWHCPWQYQYSKKJPK",
            aws_secret_access_key="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",
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3
    
s3 = s3_connection()

if s3:
    try:
        # Upload a file to the S3 bucket
        s3.upload_file("S1.csv", "odmatrix", "success.csv")
        print("File uploaded successfully!")
    except Exception as e:
        print(f"Error uploading file: {e}")