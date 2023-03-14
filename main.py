import cv2
import numpy as np

# Load the pre-trained Haar Cascade classifiers for frontal and profile faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

# Open a video capture object for the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Create a black mask with the same size as the frame
    mask = np.zeros_like(frame)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect frontal faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Copy detected frontal faces from the frame to the mask
    for (x,y,w,h) in faces:
        mask[y:y+h,x:x+w] = frame[y:y+h,x:x+w]

    # Detect profile faces in the grayscale frame
    profiles = profile_cascade.detectMultiScale(gray, 1.3, 5)

    # Copy detected profile faces from the frame to the mask
    for (x,y,w,h) in profiles:
        mask[y:y+h,x:x+w] = frame[y:y+h,x:x+w]

    # Display the resulting mask with face detections
    cv2.imshow('Face Detection',mask)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()