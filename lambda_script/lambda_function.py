import os
import boto3
import base64
import time
import json
import hashlib
import uuid
from datetime import datetime, timedelta

REGION = os.environ['REGION']
COLLECTION = os.environ['COLLECTION']
BUCKET = os.environ['BUCKET']
face_table =  os.environ['FACE_TABLE']
STREAM_RECORD = os.environ['STREAM_RECORD']
IOT_TOPIC = 'face/result'

rekognition = boto3.client("rekognition", REGION)
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
iot = boto3.client('iot-data')
face_table = dynamodb.Table(face_table)
stream_record = dynamodb.Table(STREAM_RECORD)
timeZone = 8
THRESHOLD=80

collections = rekognition.list_collections()['CollectionIds'] 
print("List rekognition collections: ",collections)

if COLLECTION not in collections:
    rekognition.create_collection(CollectionId=COLLECTION)
    print('Create collection:', COLLECTION )

# get time
def getTimestamp():
    # get timestamp
    timestamp = str(datetime.now() + timedelta(hours=timeZone))
    return timestamp

def putFaceIndex(face_id,link,name):
    face_table.put_item(
    Item={
        'face_id': face_id,
        'link': link,
        'name': name,
        'timestamp': str(getTimestamp())
    })
    return None
    
def putFaceRecord(face_id, name):
    random_id = str(uuid.uuid4())
    stream_record.put_item(
    Item={
        'record_id': random_id,
        'face_id':face_id,
        'name': name,
        'timestamp': str(getTimestamp())
    })
    return None
    
def putS3(faceDecode,key):
    response = s3.put_object(Body=faceDecode, Bucket=BUCKET, Key=key)
    return response

def lambda_handler(event, context):
    print('Source event:',event)
    image = event['face']
    
    # decode the face image
    faceDecode = base64.b64decode(image)
    
    # generate filename
    nowtime = time.strftime("%Y%m%d-%H%M%S")
    file_name = 'face-'+ nowtime + '.jpg'
    folder = 'images/'
    key = folder + file_name
    
    # put face image to S3
    response = putS3(faceDecode,key)
    print(response)
    
    # search face images on rekognition
    response = rekognition.search_faces_by_image(
		Image={
			"S3Object": {
				"Bucket": BUCKET,
				"Name": key
			}
		},
        CollectionId=COLLECTION
    )
    print("search_faces_by_image", response)
    
    # search the highest similiar face images in rekognition
    if 'FaceMatches' in response and response['FaceMatches']:
        best = response['FaceMatches'][0]
        for match in response['FaceMatches']:
            if match['Similarity'] > best['Similarity']:
                best = match
        face_id = best['Face']['FaceId']
    # if not found, create new face index
    else:
        response = rekognition.index_faces(
            Image={
                "S3Object": {
                    "Bucket": BUCKET,
                    "Name": key,
                }
            },
            CollectionId=COLLECTION
        )
        face_id = response['FaceRecords'][0]['Face']['FaceId']
    
    # try to find face_id in FaceIndex table
    try:
        response = face_table.get_item(Key={'face_id': face_id})
        name = response['Item']['name'] 
    # if face_id not found, create new index in FaceIndex table
    except KeyError:
        name = "unknown"
        link = 's3://' + BUCKET + '/' + key
        putFaceIndex(face_id, link, name)
        print("Index new face: ", face_id[-5:])
        
    # save record to FaceRecord table
    putFaceRecord(face_id,name)
    print("Face result: " ,name)
    
    # send result to iot topic 'face/result'
    print('Publish to AWS IoT Topic: face/result')
    response = iot.publish(
        topic= IOT_TOPIC,
        payload=json.dumps({
            'FaceIndex': face_id[-5:],
            'Name': name
        })
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
