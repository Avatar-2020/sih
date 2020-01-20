import json
import boto3
import base64
import datetime

exact_date=datetime.datetime.now()
parent=boto3.client('cognito-idp')
exact_date=exact_date.strftime('%x')

dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table('Accident_Case')
s3=boto3.client('s3')
invoke_lambda=boto3.client('lambda')


 
def lambda_handler(event, context):
    # TODO implement
    #the eventpart is with devansh by react native . 
    
    latitude=event['loc']['lat']
    longitude=event['loc']['long']
    device_id=event['deviceId']
    AUID=device_id+latitude+longitude+exact_date
    
    video_64_encode=event['video']
    
    video_64_encode=str.encode(video_64_encode)
    
    video_64_decode=base64.encodestring(video_64_encode)
    
    with open("/tmp/log.mp4","wb") as f:
        f.write(video_64_decode)
    s3.upload_file("/tmp/log.mp4","bucket2.sih","{}.mp4".format(AUID))
    
    #enter info in dynamo db table
    s3url='https://s3.amazonaws.com/bucket2.sih/'+'{}.mp4'.format(AUID)
    table.put_item(Item=json.dumps({'id':AUID,'lat':latitude,
    'long':longitude,'googleAdd':'https://www.google.com/maps/place/{},{}'.format(latitude,longitude)},'videoUrl':s3url))
    
    
    #Invocation of the lambda function from one lambda functions the other lambda function return the partner id 's 
    
    
    payload={"id":AUID,
    "device_id":device_id,
    "loc":[latitude,longitude]
        
        
        
    }
    resp=invoke_lambda.invoke(FunctionName='partner_list',InvocationType='Event',Payload=json.dumps(payload))
    
    
    #sending push notification to the partnerlist
    #response is our collection of data 
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
