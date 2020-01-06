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
- npm
- node.js



## Overview
<img src="images/arch.png" alt="architecture"
	 width="70%" height="70%" />


## Build
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
- Build a reactJS app
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
        - paste your api gateway endpoint on it (AWS Console -> API Gateway -> stage -> resource method)
    <img src="images/appjs.png" alt="architecture"
    width="70%" height="70%" />

    - Run npm install to load modules
    ```
    npm install
    ```
    - Run webapp server
    ```
    npm start
    ```