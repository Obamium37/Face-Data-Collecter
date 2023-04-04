import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')



# Load the image
image = cv2.imread('faces_detected.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load the face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

profile = profile_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Crop the image around the first detected face
(x, y, w, h) = faces[0]
cropped_image = image[y:y+h, x:x+w]



# Show the original image and the cropped image
cv2.imshow('Original', image)
cv2.imshow('Cropped', cropped_image)
cv2.imwrite('detected_face.jpg', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()