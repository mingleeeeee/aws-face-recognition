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
	 width="50%" height="50%" />


## Build
- Cloudformation template