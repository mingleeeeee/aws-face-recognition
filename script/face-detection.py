import dlib
import cv2
import imutils
import base64
import boto3
import json
from datetime import datetime, timedelta

IOT_TOPIC = 'face/image'
iot = boto3.client('iot-data')
def getTimestamp():
    timestamp = str(datetime.now())
    return timestamp

# Start video capturing
cap = cv2.VideoCapture(0)

# Dlib face detector
detector = dlib.get_frontal_face_detector()

# using loop to read frame from video
while(cap.isOpened()):
  ret, frame = cap.read()

  # detect faces
  face_rects, scores, idx = detector.run(frame, 0)

  # get detect results
  count = 0
  for i, d in enumerate(face_rects):
    left = d.left()
    top = d.top()
    right = d.right()
    bottom = d.bottom()
    text = "%2.2f(%d)" % (scores[i], idx[i])
    
    # frame the faces
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 4, cv2.LINE_AA)
    # mark scores
    cv2.putText(frame, text, (left, top), cv2.FONT_HERSHEY_DUPLEX,
            0.7, (255, 255, 255), 1, cv2.LINE_AA)
    
    # get height & width
    height = bottom - top
    width = right - left
    
    try:
        if height > 40 and width > 40:
            print('Face detected')
            face = frame[(top):(top + height),(left):(left + width)]
    #         if height > width:
    #             face = imutils.resize(face, width=128)
    #         else:
    #             face = imutils.resize(face, height=128)

            _, jpeg = cv2.imencode('.jpg', face)
            faceEncode = base64.b64encode(jpeg.tobytes()).decode('utf-8')
            # Publish to IoT Core Topic
            print('Publish to AWS IoT Topic: face/image\n')
            response = iot.publish(
                topic= IOT_TOPIC,
                payload=json.dumps({
                'face': faceEncode
            })
            )
            
        # frame too small
        else:
            print('face too small')
            
    except Exception as e:
        print(e)
    

  # show result
  cv2.imshow("Face Detection", frame)
  
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
