




#TODO: We need to find a way to streamline this(Website, mobile app etc..)

import cv2
import os
import time



# Capture video from the webcam
cap = cv2.VideoCapture(0)

path = 'C:/Users/tkris/Documents/Polygence Project/Face-Data-Collecter/Face_Processing Software/Faces'

times = 10

for i in range(times):

    time.sleep(1)
    ret, frame = cap.read()
    
    
    cv2.imwrite(os.path.join(path, f'face_image_{i}.jpg'), frame)


cap.release()
cv2.destroyAllWindows()
