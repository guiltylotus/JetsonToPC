# 'gst-launch-1.0 v4l2src ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink port=5000'
# filesrc location=hncloud.mp4 ! decodebin ! omxh265enc ! mpegtsmux ! tcpserversink host=192.168.1.2 port=5000
# filesrc location=test.mp4 ! decodebin ! video/x-raw,format=NV12 ! omxh265enc ! mpegtsmux ! tcpserversink host=<tx2_server_IP> port=5000 recover-policy=keyframe sync-method=latest-keyframe sync=false
# gst-launch-1.0 filesrc location=hncloud.mp4 ! decodebin ! x264enc ! mpegtsmux ! queue ! tcpserversink host=192.168.1.2 port=5000 recover-policy=keyframe sync-method=latest-keyframe sync=false
# gst-launch-1.0 filesrc location=hncloud.mp4 ! decodebin ! omxh265enc ! mpegtsmux ! tcpserversink host=192.168.1.2 port=5000

# hncloud.mp4 fps=30 shape(728, 858)
import cv2
from CloudDetect import *

# On Jetson
# fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
# out = cv2.VideoWriter('appsrc ! videoconvert ! omxh265enc ! mpegtsmux ! tcpserversink host=192.168.1.2 port=5000 sync=false', fourcc,  30.0, (w, h), True)

# On PC
cap = cv2.VideoCapture('video/hncloud.mp4')
w = 1200
h = 900
# w = 800
# h = 600

# Allow to send to client (percent %)
sendingThreshold = 30

fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter(
    'appsrc ! videoconvert ! x264enc ! mpegtsmux ! tcpserversink host=192.168.1.1 port=5000 recover-policy=keyframe sync-method=latest-keyframe sync=false', fourcc,  30.0, (w, h), True)

if (not out.isOpened()):
    print("not OKEEE")

countFrame = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret:

        frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_CUBIC)

        # Cloud Detection
        if (countFrame < 1):
            threshold = Kmean(frame)
        cloudFrame = CloudThreshold(frame, threshold)
        totalCloud = TotalCloud(frame, threshold)

        # percent Cloud
        percetCloud = round(totalCloud/(w*h) * 100, 0)
        if (percetCloud > sendingThreshold):
            print('Frame: ' + str(countFrame) + ' has ' +  str(percetCloud) + '%' + ' will not send')
        else:
            print('Frame: ' + str(countFrame) + ' has ' +  str(percetCloud) + '%' + ' will send')
            out.write(frame)

        # Show
        cv2.imshow('sender', cloudFrame)
        countFrame = countFrame + 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
