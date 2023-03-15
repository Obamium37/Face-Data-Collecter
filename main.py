
#I changed the system last minute so ignore all warnings about buggy code



import cv2
import numpy as np

# Load the pre-trained Haar Cascade classifiers for frontal and profile faces
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

# Open a video capture object for the webcam
cap = cv2.VideoCapture(0)


while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    
    

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    profileCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface_default.xml")
    profile = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    print("[INFO] Found {0} Faces!".format(len(faces)))
    print("[INFO] Found {0} Faces!".format(len(profile)))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    for (x, y, w, h) in profile:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        

    status = cv2.imwrite('faces_detected.jpg', frame)
    print("[INFO] Image faces_detected.jpg written to filesystem: ", status)




    

    # Display the resulting mask with face detections
    cv2.imshow('Face Detection',frame)

   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
