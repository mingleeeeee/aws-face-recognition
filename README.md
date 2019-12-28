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


## Build
- AWS Credential Configure
    - Enter access id, secret access key, default region name, default output format
```
aws configure
```
- Cloudformation template (This will build whole architecture of AWS resources)
    - Open AWS console
    - Go to `Cloudformation`
    - Click `Create stack`
    - Click `Upload`
    - Select `cf.yaml` in `/aws_script/cf_template`

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
    - Cognito
    - API Gateway
```
react
```