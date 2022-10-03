import json
import uuid
    
def lambda_handler(event, context):
    import codecs
    from boto3 import Session
    from boto3 import resource

    session = Session(region_name="ap-south-1")
    polly = session.client("polly")
    
    s3 = resource('s3')
    bucket_name = "expressapi"
    bucket = s3.Bucket(bucket_name)
    
    # filename = json.loads(event['body'])["filename"]
    filename = f"{str(uuid.uuid4())}.mp3"
    myText = json.loads(event['body'])["text"]
    voice = json.loads(event['body'])["voice"]
    
    response = polly.synthesize_speech(
    Text=myText,
    OutputFormat="mp3",
    VoiceId=voice)
    stream = response["AudioStream"]
    
    bucket.put_object(Key=filename, Body=stream.read())
    
    url = f"https://xf8iic84h8.execute-api.ap-south-1.amazonaws.com/expressapi/download?filename={filename}"
    
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps({"message": "Success", "url": url})
    
    return responseObject
