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


#sns = boto3.client('sns',region_name="us-east-2")
#msg = "Hi, How are you? This is a mail for your latest pushed s3 object. Consider this url as #presigned URL \
#NOTE: This S3 object link will expire after 5 mins. You will need to contact our team incase you #want the recording."\ 
#response = sns.publish(TopicArn='arn:aws:sns:us-east-2:673304395320:SES_EC2',Message= msg + url)
#print(response)

#========================This is working===============================
ses = boto3.client('ses',region_name="us-east-2")#,config=Config(X-Amz-Algorithm==AWS4-HMAC-SHA256,X-AMZ-Expires==300))
response = ses.send_email(
    Source='jlimbachiya@safetyvision.com',
    Destination={
        'ToAddresses': ['jeet.limbachiya@relayhumancloud.com','jeet@svcloud.live']
    },
    Message={
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'Sending a URL of S3  ',# +  f'URL: {url}'),
            'Charset': 'UTF-8'
        },
        'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': 'Below is a URL of S3  'f'URL: {url}',
            'Charset': 'UTF-8'
          }
        }
})

print(response)

#=========================This is also working===============================

import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Setup the basics here
SENDER = "JL <jeet@svcloud.live>"
#RECIPIENT = "jeet.limbachiya@relayhumancloud.com"
SUBJECT = "Sending a URL of S3 object alongwith video file"

# The configuration set used to track mails
#CONFIGURATION_SET = "ConfigSet"

# The full path to the file that will be attached to the email.
ATTACHMENT = "/home/ubuntu/AWS-FaceBlurring/AWS_FB/Output.mp4"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = "Hello,\r\nBelow is a URL of S3 object of f'date: {d}'."

# The HTML body of the email.
BODY_HTML =f"Below is a URL of S3 object of date: {d}\n: " + url #"""\
#<html>
#<head></head>
#<body>
#<h1>Hello!</h1>
#<p>Below is a URL of S3 object of f"date: {d}"</p>
#<a href=url>Cick here</arrr>
#</body>
#</html>
#"""

# The character encoding for the email.
CHARSET = "utf-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses')

# Create an instance of multipart/mixed parent container.
msg = MIMEMultipart('mixed')

# Add subject, from and to lines.
msg['Subject'] = SUBJECT
msg['From'] = SENDER
#msg['To'] = RECIPIENT

# Create a multipart/alternative child container.
msg_body = MIMEMultipart('alternative')

# Encode the text and HTML content and set the character encoding. This step is
# necessary if you're sending a message with characters outside the ASCII range.
textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

# Add the text and HTML parts to the child container.
msg_body.attach(textpart)
msg_body.attach(htmlpart)

# Define the attachment part and encode it using MIMEApplication.
att = MIMEApplication(open(ATTACHMENT, 'rb').read())
# Add a header to tell the email client to treat this part as an attachment,
# and to give the attachment a name.
att.add_header('Content-Disposition','attachment',filename=os.path.basename(ATTACHMENT))

# Attach the multipart/alternative child container to the multipart/mixed
# parent container.
msg.attach(msg_body)

# Add the attachment to the parent container.
msg.attach(att)
#print(msg)
try:
    #Provide the contents of the email.
    response = client.send_raw_email(
        Source=SENDER,
        Destinations=[ jeet.limbachiya@relayhumancloud.com','jeet@svcloud.live','shrikant.viswanathan@relayhumancloud.com'

            #RECIPIENT
        ],
        RawMessage={
            'Data':msg.as_string(),
        },
       # ConfigurationSetName=CONFIGURATION_SET
    )
# Display an error if something goes wrong.
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])

#=====================================================




# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# sender_email = "sv2022relayhumancloud@gmail.com"
# receiver_email = "jeet.limbachiya@relayhumancloud.com"
# password = input("Type your password and press enter:")

# message = MIMEMultipart("alternative")
# message["Subject"] = "S3 object URL testing"
# message["From"] = sender_email
# message["To"] = receiver_email


# # Create the plain-text and HTML version of your message
# text = "\
# Hi ,\
# How are you?\
# This is a mail for your latest pushed s3 object. \
# NOTE: This S3 object link will expire after 5 mins. You will need to contact our team incase you want the recording. "
# html = url
# # Turn these into plain/html MIMEText objects
# part1 = MIMEText(text, "plain")
# part2 = MIMEText(html, "html")

# # Add HTML/plain-text parts to MIMEMultipart message
# # The email client will try to render the last part first
# message.attach(part1)
# message.attach(part2)

# # Create secure connection with server and send email
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(
#         sender_email, receiver_email,message.as_string()
#     )
