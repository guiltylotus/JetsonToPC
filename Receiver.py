import numpy as np
import cv2
import math

# cap = cv2.VideoCapture("rtsp://192.168.10.103:8554/test")
# cap = cv2.VideoCapture("rtsp://192.168.1.2:8554/test")
cap = cv2.VideoCapture("tcp://192.168.1.1:5000")
# cap = cv2.VideoCapture('udpsrc port=5000 caps="application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
# cap = cv2.VideoCapture("udpsrc port=5000 ! application/x-rtp,media=video,payload=96,clock-rate=90000,encoding-name=H264, ! rtph264depay ! decodebin ! videoconvert ! video/x-raw, format=BGR ! appsink ")
# cap = cv2.VideoCapture('udp://127.0.0.1:5000')
# cap = cv2.VideoCapture("udp://192.168.1.2:5000")

if (cap.isOpened() == False):
    print('Can not open Camera')

count = 0

while(True):

    # Capture frame-by-frame
    ret, frame = cap.read()

    count += 1

    cv2.imshow('frame2', frame)
    cv2.imwrite('receive/' + str(count) + '.png', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
