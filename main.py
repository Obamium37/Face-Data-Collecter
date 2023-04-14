





#TODO: Only takes one picture, we need it to take multiple


import cv2
import os
import time



# Capture video from the webcam
cap = cv2.VideoCapture(0)

path = 'C:/Users/tkris/Documents/Polygence Project/Face-Data-Collecter/Faces'

    

for i in range(3):

    time.sleep(1)
    ret, frame = cap.read()
    
    
    cv2.imwrite(os.path.join(path, f'face_image_{i}.jpg'), frame)


cap.release()
cv2.destroyAllWindows()
