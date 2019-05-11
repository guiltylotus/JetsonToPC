# 'gst-launch-1.0 v4l2src ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink port=5000'
# filesrc location=hncloud.mp4 ! decodebin ! omxh265enc ! mpegtsmux ! tcpserversink host=192.168.1.2 port=5000
# filesrc location=test.mp4 ! decodebin ! video/x-raw,format=NV12 ! omxh265enc ! mpegtsmux ! tcpserversink host=<tx2_server_IP> port=5000 recover-policy=keyframe sync-method=latest-keyframe sync=false
# gst-launch-1.0 filesrc location=hncloud.mp4 ! decodebin ! x264enc ! mpegtsmux ! queue ! tcpserversink host=192.168.1.2 port=5000 recover-policy=keyframe sync-method=latest-keyframe sync=false
# gst-launch-1.0 filesrc location=hncloud.mp4 ! decodebin ! omxh265enc ! mpegtsmux ! tcpserversink host=192.168.1.2 port=5000

# hncloud.mp4 fps=30 shape(728, 858)
import cv2

# # True
# cap = cv2.VideoCapture("v4l2src ! video/x-raw, framerate=30/1, width=640, height=480 ! appsink")
# out = cv2.VideoWriter("appsrc ! videoconvert ! x264enc ! rtph264pay ! udpsink port=5000", 0,  30.0, (640, 480))

#cap = cv2.VideoCapture("filesrc location=video/hncloud.mp4 ! decodebin ! videoconvert ! appsink", cv2.CAP_GSTREAMER)
#out = cv2.VideoWriter("appsrc ! queue ! videoconvert ! omxh265enc ! mpegtsmux ! tcpserversink host=192.168.1.2 port=5000", 0,  30.0, (858, 728), True)

#cap = cv2.VideoCapture("v4l2src ! video/x-raw, framerate=30/1, width=858, height=728 ! appsink")
#out = cv2.VideoWriter('appsrc ! queue ! videoconvert ! video/x-raw ! omxh264enc ! video/x-h264 ! h264parse ! mpegtsmux ! tcpserversink host=192.168.1.2 port=5000',0,25.0,(858,728))

#cap = cv2.VideoCapture("v4l2src ! video/x-raw, framerate=30/1, width=640, height=480 ! appsink")
#out = cv2.VideoWriter("appsrc ! videoconvert !x264enc ! mpegtsmux ! queue ! tcpserversink host=192.168.1.2 port=5000 recover-policy=keyframe sync-method=latest-keyframe sync=false", 0,  30.0, (640, 480))

#cap = cv2.VideoCapture("filesrc location=video/hncloud.mp4 ! decodebin ! videoconvert ! appsink")
#out = cv2.VideoWriter("appsrc ! videoconvert !x264enc ! mpegtsmux ! queue ! tcpserversink host=192.168.1.2 port=5000 recover-policy=keyframe sync-method=latest-keyframe sync=false", 0,  30.0, (858, 728))

cap = cv2.VideoCapture('video/hncloud.mp4')
w = 800
h = 600

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter('appsrc ! videoconvert ! omxh265enc ! mpegtsmux ! tcpserversink host=192.168.1.2 port=5000 sync=false', fourcc,  30.0, (w, h), True)

if (not out.isOpened()):
    print("not OKEEE")

# Define the codec and create VideoWriter object
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        #frame = cv2.flip(frame, 0)

        # __________________________Find FPS
        # fps = cap.get(cv2.CAP_PROP_FPS)
        # print("Frames per second using cap.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
        # # _____________________________________________________________
        # print('shape', frame.shape)
        frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_CUBIC)
        cv2.imshow('sender', frame)
        out.write(frame)
        # cv2.imshow('sender', out)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
