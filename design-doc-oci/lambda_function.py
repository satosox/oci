import json
import boto3
import os
import oci
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    try:
        apitable = dynamodb.Table('apikey')
        clientip = event["requestContext"]["identity"]["sourceIp"]
        
        val = apitable.query(KeyConditionExpression=Key('ip').eq(clientip))
        pri_key = val["Items"][0]["pri"]
        
        path = '/tmp/pri_key.pem'
        
        with open(path, mode='w') as f:
            f.write(pri_key)
       
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
        
    except:
        import traceback
        traceback.print_exc()
        
        print("Error!")
        
        return {
        'statusCode' : 500,
        'body' : 'Error! Again.'
    }
