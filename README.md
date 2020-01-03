# aws-face-recognition
This workshop let you use AWS resources to build a complete face recognition application.

## Prerequisite
This workshop requires the following:
- AWS Account with sufficient privileges
- Computer/Laptop and webcam 
- Python library
    - python-opencv
    - dlib
    - boto3
    - awscli
    ``` 
    pip install -r requirement.txt 
    ```
- [Docker](https://hub.docker.com/?overlay=onboarding)
- npm
- node.js



## Overview
- Data Ingestion
    - Batch
        - AWS Glue
        - AWS Batch
    - Realtime
        - AWS IoT
        - AWS Kinesis Firehose

- Data Consumption
    - React & Amplify
    - AWS API Gateway & Lambda

- ML Application
    - AWS Rekognition

<img src="images/arch.png" alt="architecture"
	 width="70%" height="70%" />


## Build realtime processing flow
- AWS Credential Configure
    - Enter access id, secret access key, default region name, default output format
```
aws configure
```
- Cloudformation template (This will build AWS resources)
    - Open AWS console
    - Go to **S3**
        - Click create bucket
        - Enter a **unique** bucket name
        - Click **create**
        - Upload **lambda_script** folder to S3 in **aws_script**
        <img src="images/s3.png" alt="architecture"
	 width="70%" height="70%" />

    - Go to **Cloudformation**
        - Click **Create stack**
        - Click **Upload**
        - Select `cf.yaml` in **/aws_script/cf_template**

- AWS Console setting
    - API Gateway CORS setting
        - Go to **API Gatway**
        - Select **Lab-API**
        - Click **Resources** on the left panel
        - Click **/lab** on the mid panel
        - Click **Actions**, and select **Enable CORS**
        - Click **Enable CORS and replace existing CORS headers**
        - Click **Yes,replace existing values**

- Face detection app (Requires local computer/laptap with webcam)
    - This will start a face detection app
    - Detected faces will be saved as jpg and send to AWS IoT Topic
    - Default IoT Topic name is `face/image`. You can change it, but note that `IoT Rule` need to subscribe to this topic.
```
cd script
python face-detection.py
```
- ReactJS app
    - Build app
        - [Documentation please Refer to here](https://aws-amplify.github.io/docs/js/start)
        - Basic installation
        ```
        npx create-react-app webapp
        cd webapp
        npm install @aws-amplify/api @aws-amplify/pubsub
        npm install aws-amplify-react
        # Setup backend
        amplify init
        amplify status
        amplify push
        ```
        - Copy files in **react_script** folder to **webapp**
            - package.json
            - public
            - src
        - Edit `App.js` in **webapp/src**
            - paste your api gateway endpoint on it
        <img src="images/appjs.png" alt="architecture"
	 width="70%" height="70%" />
        - run npm install
        ```
        npm install
        ```
        - run webapp server
        ```
        npm start
        ```

## Build batch processing flow
- RDS setup
    - Go to **AWS RDS** console
    - Click **Create database** on the upper-right corner
    - For **Engine options**, select **MySQL**
    - For **Templateds**, choose **Free tier**
    - For **Settings**
        - For **DB instance identifier**, type in `face-database`
        - For **Credentials Settings**, select **Auto generate a password**
        - The others keep in default
    - Click **Create database**

- Glue setup
    - Go to **AWS Glue` console**
    - Click **Jobs** on the left panel
    - Click **Add job**
        - For **Name**, enter `face-job`
        - For **IAM role**, select **Lab-glue-serive-role**
        - For **Type**, select **Spark**
        - For **Glue version**, select **Spark2.4, python3**
        - For **This job runs**, select **A new script to be authored by you**
        - For **Script file name**, enter `batch-job`
        - Click **Save job and edit script**
        - Paste and edit the code

        ```
        import boto3
        import pymysql
        import base64
        import json
        import time
        import csv
        import sys
        from awsglue.transforms import *
        from awsglue.utils import getResolvedOptions
        from pyspark.context import SparkContext
        from awsglue.context import GlueContext
        from awsglue.job import Job

        glueContext = GlueContext(SparkContext.getOrCreate())
        s3 = boto3.client('s3')

        ## edit here ##
        BUCKET = "Your bucket name"
        HOST = 'Your database Endpoint'
        PASSWD = 'YourPassword'
        DB = 'face-db'
        ###############

        conn = pymysql.connect (host = HOST,
                                user = 'admin',
                                passwd = PASSWD,
                                db = DB ) 
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
        ```

        - Click **Save**
        - Click **Run job**

- Batch setup
    - ECR setting
        - Click **Create repository**
        - For **Repository name**, enter `batch-job`
        - Click **Create repository**
        - Select `batch-job`
        - Click **View push commands** on the top panel
        - Use commands to build docker image and push to ECR
    - Compute environments
        - Click **Create environment**
        - For **Compute environment name**, enter `Batch-environment`
        - For **Service role**, select `lab-batch-job`
        - For **Instance role**, select `Create new role`
        - Click **Create**
    - Job queues
        - Click **Create queue**
        - For **Queue** name, enter `Lab-job-queue`
        - For **Priority**, enter `1`
        - For **Connected compute environments for this queue**, select `lab-batch-job`
        - Click **Create job queue**
    - Job definitions
        - Click **Job definition** on the left panel
        - Click **Create**
        - For **Job definition name**, enter `read-database`
        - For **Job role**, select `Lab-ecs-batch-role`
        - For **Container image**, enter the image uri in **ECR**
        - For **Command**, keep it empty.
        - Click **Create Job Definition**
    - Jobs
        - Click **Jobs** on the left panel
        - Click **Submit jobs**
        - For **Job name**, enter `batch-job`
        - For **Job definition**, select the latest `read-database`
        - For **Job queue**, select `Lab-job-queue`
        - Others keep in default
        - Click **Submit job**
