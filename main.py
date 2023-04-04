





#TODO: Only takes one picture, we need it to take multiple


import cv2

# Load the pre-trained face detection classifier

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Loop through each frame
while True:
    # Read the frame
    ret, frame = cap.read()

    cv2.imshow('frame', frame)
    cv2.imwrite('faces_detected.jpg', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
