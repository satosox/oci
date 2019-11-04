import json
import boto3
import os
import oci
import urllib
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    try:
        apitable = dynamodb.Table('apikey')
        clientip = event["requestContext"]["identity"]["sourceIp"]
        
        val = apitable.query(KeyConditionExpression=Key('ip').eq(clientip))
        pri_key = val["Items"][0]["pri"]
        
        param = urllib.parse.parse_qs(event['body'])
        
        user_id = param["user"][0]
        path = '/tmp/pri_key.pem'
        fingerprint = param["finger"][0]
        tenancy_id = param["tenancy"][0]
        region = param["region"][0]
        namespace = param["namespace"][0]
        compartment = param["compartment"][0]
        
        with open(path, mode='w') as f:
            f.write(pri_key)
        
        config = {
            "user": user_id,
            "key_file": path,
            "fingerprint": fingerprint,
            "tenancy": tenancy_id,
            "region": region
        }
        
        ob_sto = oci.object_storage.ObjectStorageClient(config)
        oci_ob = vars(ob_sto.list_buckets(namespace_name=namespace,compartment_id=compartment))
        
        print(oci_ob["data"][0])
        
        return {
            'statusCode': 200,
            'body': 'OK!'
        }
        
    except:
        import traceback
        traceback.print_exc()
        
        print("Error!")
        
        return {
        'statusCode' : 500,
        'body' : 'Error! Again.'
    }
