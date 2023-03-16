import json
import uuid
import codecs
from boto3 import Session, resource, client
    
def lambda_handler(event, context):
    session = Session(region_name="ap-south-1")
    polly = session.client("polly")
    
    s3 = resource('s3')
    bucket_name = "expressapi"
    bucket = s3.Bucket(bucket_name)
    # filename = json.loads(event['body'])["filename"]
    filename = f"{str(uuid.uuid4())}.mp3"
    request = json.loads(event["body"])
    
    response = polly.synthesize_speech(
        Engine = "neural",
        Text=request["text"],
        LanguageCode=request["language"],
        OutputFormat="mp3",
        VoiceId=request["voice"]
    )
    
    stream = response["AudioStream"]
    
    bucket.put_object(Key=filename, Body=stream.read())
    
    url = f"https://expressapi.s3.ap-south-1.amazonaws.com/{filename}"
    
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps({"message": "Success", "url": url})
    
    return responseObject
