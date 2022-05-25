from datetime import datetime        
import boto3
from boto3 import client
from botocore.client import Config

m = datetime.now().minute
h = datetime.now().hour
d = datetime.now().date()

s3 = boto3.client('s3')
Now = f"{d}, {h}:{m}"
with open("Students_1.mp4","rb") as f:
    s3.upload_fileobj(f, "faceredactionbucket",f"Output - {Now}.mp4",ExtraArgs={'ContentType': 'video/mp4'})


s3 = client('s3', region_name="us-east-2", config=Config(signature_version='s3v4'))
url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={'Bucket': 'faceredactionbucket', 'Key': f"Output - {Now}.mp4"},
    ExpiresIn=360,
    )

print(url)





import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "sv2022relayhumancloud@gmail.com"
receiver_email = "jeet.limbachiya@relayhumancloud.com"
password = input("Type your password and press enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "S3 object URL testing"
message["From"] = sender_email
message["To"] = receiver_email


# Create the plain-text and HTML version of your message
text = "\
Hi ,\
How are you?\
This is a mail for your latest pushed s3 object. \
NOTE: This S3 object link will expire after 5 mins. You will need to contact our team incase you want the recording. "
html = url
# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email,message.as_string()
    )
