import json
import boto3
import math
import csv

s3=boto3.client('s3')


def min_geo(partner_list,loc):
    #partner_list is 2d array
    #loc is 1d array 
    w1=0
    w2=0
    dif_w=0
    dif_l=0
    a=0
    darr=[]
    for i in range(len(partner_list[0])):
        w1=math.radians(float(partner_list[i][1]))
        w2=math.radians(loc[0])
        dif_w=w2-w1
        dif_l=math.radians(loc[1]-float(partner_list[i][2]))
        a=pow(math.sin(dif_w/2),2)+math.cos(w1)*math.cos(w2)*pow(math.sin(dif_l/2),2)
        c=math.atan2(math.sqrt(a),math.sqrt(1-a))*2
        d=c*6371
        d=round(d,2)
        darr.append(d)

    return darr 
    #darr returning the distance in km from acc place to the partners distance
    

#event function give the {"loc":[22.7838,77.35366]}

def lambda_handler(event, context):
    
    bucket = ['Record'][0]['s3']['bucket']['name']
    file_key = ['Record'][0]['s3']['object']['key']
    
    csvfile = s3.get_object(Bucket=bucket, Key=file_key)
    csvcontent = csvfile['Body'].read().split(b'\n')
        
    #part_id,latitude,longitude
        
    data = []
    with open(csvfile['Body'], 'r') as csv_file:
        
        csv_file = csv.DictReader(csv_file)
        data = list(csv_file)
    
    #data is the matrix 
    
    latitude=event['loc'][0]
    longitude=event['loc'][1]
    acc_loc=[latitude,longitude]
    not_matrix=function(data,acc_loc)
        
    #send the notification to these partners
    
    
    #hence final list is the distance in km
    #select that distance whose have in range of 30km
    index=[]
    for i in range(len(final_lis)):
        
        if final_lis[i]<30:
        index.append(i)


    print(index)

    notification_bhej=[]
    for i in range(len(index)):
        notification_bhej.append(partner_list[index[i]])


    print(notification_bhej) 
        
    #notification bhej is the matrix : 
    
    #for i in range(len(notification_bhej[0])):
    #   print(notification_bhej[i])
    token_list=[]
    for i in range(len(notification_bhej[0])):
        token_list.append(notification_bhej[i][3])
        
        
        
    
    #acc_loc is the list having 2 elements latitude=acc_loc[0],longitude=acc_loc[1]
    #token_list is the list of tokens
    #notification_to_partners = [['kmc_hosp',22.34,77.766],['olpolice',22.345,76.66],['firestatin',22.345,76.66]]
    #acc_loc=[22.34,67.67]
    data={
        'device_id':event['device_id']
        'AUID':event['id']
        'notification_to_partners':notification_bhej
        'token':token_list
        'target_loc':acc_loc
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
