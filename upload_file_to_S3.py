        
import boto3
s3 = boto3.client('s3')
with open("Students_1.mp4","rb") as f:
    s3.upload_fileobj(f, "faceredactionbucket","Students_1.mp4")


from boto3 import client
from botocore.client import Config

s3 = client('s3', region_name="us-east-2", config=Config(signature_version='s3v4'))
url = s3.generate_presigned_url(
    ClientMethod='get_object',
        Params={'Bucket': 'faceredactionbucket', 'Key': 'Students_1.mp4'},
        ExpiresIn=3600,
    )

print(url)


