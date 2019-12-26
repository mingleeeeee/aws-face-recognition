import boto3
import pymysql
import base64
import json
import time
#import csv
import os

BUCKET = os.environ['BUCKET'] 
HOST = os.environ['HOST']
USER = os.environ['USER']
PASSWD = os.environ['PASSWD']
DB = os.environ['DB'] #face-db

s3 = boto3.client('s3')
conn = pymysql.connect (host = HOST, user = USER, passwd = PASSWD, db = DB ) 
cur = None
if conn is not None:
    cur = conn.cursor()
if cur is not None:
    cur.execute("select * from `face-table`")
    for  r  in  cur: 
        #print(r[1])
        image = r[1]
        faceDecode = base64.b64decode(image)

        nowtime = time.strftime("%Y%m%d-%H%M%S")
        file_name = 'face-'+ nowtime + '.jpg'
        folder = 'images/'
        uploadPath = folder + file_name
        response = s3.put_object(Body=faceDecode, Bucket=BUCKET, Key= uploadPath)
        print(response) 
     
#     save to csv
#     with open('test.csv', 'w', newline='') as myfile:
#         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#         for  r  in  cur: 
#             wr.writerow(r)
#         print(wr)
#     with open('test.csv','rb') as csvfile:
#         response = s3.put_object(Body=csvfile, Bucket=BUCKET, Key= 'csv/RDS.csv')
    conn.commit()
cur.close() 
conn.close()
