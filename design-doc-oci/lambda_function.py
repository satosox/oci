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
        
        compute = oci.core.ComputeClient(config)
        oci_compute = vars(compute.list_instances(compartment_id=compartment))
        
        result_compute = '<h2>Compute Instances</h2>'
        
        for i in range(len(oci_compute["data"])):
            result_compute += oci_compute["data"][i].display_name + "<br>"
        
        ob_sto = oci.object_storage.ObjectStorageClient(config)
        oci_ob = vars(ob_sto.list_buckets(namespace_name=namespace,compartment_id=compartment))
        
        result_os = '<h2>ObjectStorage Buckets</h2>'
        
        for i in range(len(oci_ob["data"])):
            result_os += oci_ob["data"][i].name + "<br>"
        
        result = result_compute + result_os
        
        return {
            'statusCode': 200,
            'headers' : {
                'content-type' : 'text/html'
            },
            'body' : result
        }
        
    except:
        import traceback
        traceback.print_exc()
        
        print("Error!")
        
        return {
        'statusCode' : 500,
        'body' : 'Error! Again.'
    }
