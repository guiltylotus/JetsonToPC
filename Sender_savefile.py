# import numpy as np
# import cv2

# cap = cv2.VideoCapture(0)

# # Get the Default resolutions
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))

# # Define the codec and filename.
# out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret==True:

#         # write the  frame
#         out.write(frame)

#         cv2.imshow('frame',frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break

# # Release everything if job is finished
# cap.release()
# out.release()
# cv2.destroyAllWindows()

# _______________________________________________________

import numpy as np
import cv2

cap = cv2.VideoCapture('video/hncloud.mp4')
w = 800
h = 600

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter('video/output.mp4', fourcc, 25, (w, h), True)
count = 0
while(cap.isOpened()):
    count = count + 1
    print ("processing frame ", count)
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_CUBIC)
        y_len, x_len, _ = frame.shape


        out.write(frame)


cap.release()
out.release()
cv2.destroyAllWindows()
