import boto3
s3 = boto3.client('s3')
with open("Output.mp4","rb") as f:
    s3.upload_fileobj(f, "fbwithoutbucket","Output.mp4")

url = boto3.client('s3').generate_presigned_url(
    ClientMethod='get_object',
    Params={'Bucket': 'faceredactionbucket', 'Key': 'ezgif.com-gif-maker (1).gif'},
    ExpiresIn=3600)

print("This is URL:",url)


#class Upload:

#    def __init__(self, s3bucket, output):
#        self.s3bucket = s3bucket
#        self.output = output

#        self.s3 = boto3.client('s3')

#    if __name__=='__main__':
#        with open(self.output, "rb") as f:
#          self.s3.upload_fileobj(f, self.s3bucket, self.output)
