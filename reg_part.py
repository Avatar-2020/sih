import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64

USER_POOL_ID='ap-south-1_9lZQtsYpN' 
CLIENT_ID=' 4hdh2anmct7r0hjfpn2kqpvpsb'
CLIENT_SECRET='1hplutaifmqu7d2gvi90987p17svb5t3velpaaq27mv2ehm3m0bo'


dynamodb=boto3.resource('dynamodb')

table=dynamodb.Table('partner_info')

'''
in this we post the item to dynamodb table 

  having JSON formats 
  
  json.dumps(
  {
      'username':username,
      'lat':lat,
      'long':longi
      
  }
  )





'''


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
    msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
def lambda_handler(event, context):    
    for field in ["username", "email", "password","custom:type","custom:lat","custom:long","custom:zip"]:
        if not event.get(field):
            return {"error": False, "success": True, 'message': f"{field} is not present", "data": None}
    username = event['username']
    email = event["email"]
    password = event['password']
    lat = event["custom:lat"]
    longi=event["custom:long"]
    addr=event['custom:zip']
    type_part=event['custom:type']
    
    table.put_item(Item=json.dumps({'username':username,
      'lat':lat,
      'long':longi}))
    
    client = boto3.client('cognito-idp')    
    try:
        
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password, 
            UserAttributes=[
            {
                'Name': "custom:zip",
                'Value': addr
            },
            {
                'Name': "email",
                'Value': email
            },
            {
                'Name': "custom:type",
                'Value': type_part
            },
            {
                'Name': "custom:lat",
                'Value': lat
            }
            {
                'Name': "custom:long",
                'Value': longi
            }
            ],
            ValidationData=[
                {
                'Name': "email",
                'Value': email
            },
            {
                'Name': "custom:username",
                'Value': username
            }])
    
    
    except client.exceptions.UsernameExistsException as e:
        return {"error": False, 
               "success": True, 
               "message": "This username already exists", 
               "data": None}
    except client.exceptions.InvalidPasswordException as e:
        
        return {"error": False, 
               "success": True, 
               "message": "Password should have Caps,\
                          Special chars, Numbers", 
               "data": None}    
    except client.exceptions.UserLambdaValidationException as e:
        return {"error": False, 
               "success": True, 
               "message": "Email already exists", 
               "data": None}
    
    except Exception as e:
        return {"error": False, 
                "success": True, 
                "message": str(e), 
               "data": None}
    
    return {"error": False, 
            "success": True, 
            "message": "Please confirm your signup, \
                        check Email for validation code", 
            "data": None}
    
    
    
    
    return {
        "code":200,
        "message":"Not working properly . "
    }

