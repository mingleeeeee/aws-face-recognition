FROM python:3

ADD job.py /

RUN pip install boto3 pymysql

CMD [ "python", "./job.py" ]
