# 'gst-launch-1.0 v4l2src ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink port=5000'

# hncloud.mp4 fps=30 shape(728, 858)
import cv2

# # True
# cap = cv2.VideoCapture("v4l2src ! video/x-raw, framerate=30/1, width=640, height=480 ! appsink")
# out = cv2.VideoWriter("appsrc ! videoconvert ! x264enc ! rtph264pay ! udpsink port=5000", 0,  30.0, (640, 480))

cap = cv2.VideoCapture(
    "filesrc location=video/hncloud.mp4 ! decodebin ! video/x-raw ! videoconvert ! appsink")
out = cv2.VideoWriter(
    "appsrc ! videoconvert ! x264enc ! rtph264pay ! tcpserversink host=192.168.1.1 port=5000", cv2.VideoWriter_fourcc('M','J','P','G'),  30.0, (858, 728))

# cap = cv2.VideoCapture('video/hncloud.mp4')

# Define the codec and create VideoWriter object

if (out.isOpened()):
    print('oOKEE')

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 0)

        # __________________________Find FPS
        # fps = cap.get(cv2.CAP_PROP_FPS)
        # print("Frames per second using cap.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
        # # _____________________________________________________________
        # print('shape', frame.shape)
        # write the flipped frame
        # cv2.imshow('sender', frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
