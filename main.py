#I changed the system last minute so ignore all warnings about buggy code





#TODO: Only takes one picture, we need it to take multiple


import cv2

# Load the pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Loop through each frame
while True:
    # Read the frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    profile = profile_cascade.detectMultiScale(gray, 1.3, 5)

    # Loop through each face and draw a bounding box
    for (x, y, w, h) in faces:
        # Draw a green rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Set everything outside of the bounding box to black
        frame[:, :x] = 0
        frame[:, x+w:] = 0
        frame[:y, x:x+w] = 0
        frame[y+h:, x:x+w] = 0

    for (x, y, w, h) in profile:
        # Draw a green rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Set everything outside of the bounding box to black
        frame[:, :x] = 0
        frame[:, x+w:] = 0
        frame[:y, x:x+w] = 0
        frame[y+h:, x:x+w] = 0

    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imwrite('faces_detected.jpg', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and destroy the window
cap.release()
cv2.destroyAllWindows()
