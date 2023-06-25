import cv2
import os

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

path = 'C:/Users/tkris/Documents/Polygence Project/Face-Data-Collecter/Face_Processing Software\Faces'

num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
print(num_files)


# Load the image

for i in range(num_files):
    image = cv2.imread(os.path.join(path, f'face_image_{i}.jpg') )

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

    save_path = 'C:/Users/tkris/Documents/Polygence Project/Face-Data-Collecter/Faces_edited'
    cv2.imwrite(os.path.join(save_path, f'face_detected_{i}.jpg'), cropped_image)


