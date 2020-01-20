import json
import json
import boto3

#GET REQUEST
TABLE_NAME='accident_info'

#have to enter the particular id - AUID

#AUID= device_id+longitude+latitude+exact_date 

dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table(TABLE_NAME)

#note that event will give only the accident unique id : 
'''
{
   "id":AUID 
    
}

'''

def lambda_handler(event, context):
    
    response=table.get_item(Item=event['id'])
    print(response['Item'])
    
    return {
        'statusCode': 200,
        'message':'get info about accident . '
    }
