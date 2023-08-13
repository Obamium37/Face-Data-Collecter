import cv2
import time
import numpy as np
import imutils
import dlib
from scipy.spatial import distance as dist
from deepface import DeepFace

# List of available models, backends, and metrics
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe', 'yolov8', 'yunet']
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
metrics = ["cosine", "euclidean", "euclidean_l2"]

# Initialize dlib's face detector (HOG-based) and the facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Indexes of facial landmarks for the left and right eye
(lStart, lEnd) = (42, 48)
(rStart, rEnd) = (36, 42)

# Motion detection settings
width = 700
min_area = 3000
frame_count = 30  # Number of frames to pass before motion detection is considered true

def capture_image(image_path):
    # Capture a single frame
    ret, frame = cap.read()

    # If frame is read correctly, ret is True
    if not ret:
        print("Can't receive frame. Exiting ...")
        exit()

    # Save the frame as an image
    cv2.imwrite(image_path, frame)

def eye_aspect_ratio(eye):
    # Compute the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    return ear

def detect_blink(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    rects = detector(gray, 0)

    # Loop over the face detections
    for rect in rects:
        # Determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = np.array([(shape.part(i).x, shape.part(i).y) for i in range(0, 68)])

        # Extract the left and right eye coordinates
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        # Compute the eye aspect ratio for both eyes
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # The average eye aspect ratio
        ear = (leftEAR + rightEAR) / 2.0

        # Check if the eye aspect ratio is below the blink threshold, and if so, increment the blink frame counter
        if ear < 0.3:
            return True

    return False


def verify_faces(captured_image_path, image_paths):
    verification_successful = False
    # Loop over the verification images
    for image_path in image_paths:
        try:
            # Use DeepFace to verify the images
            result = DeepFace.verify(img1_path = image_path, 
                                     img2_path = captured_image_path, 
                                     model_name = models[2],
                                     distance_metric = metrics[2],
                                     detector_backend = backends[1])#4

            # Print the result
            print(f"Is the captured image the same person as in {image_path}?: ")
            if result['verified'] == True:
                print("Yes")
                verification_successful = True
                # Break from the loop, but keep going if you want to check all faces
            else:
                print("No")

            # Draw bounding box
            image = cv2.imread(captured_image_path) 

            x = result['facial_areas']['img2']['x']
            y = result['facial_areas']['img2']['y']
            w = result['facial_areas']['img2']['w']
            h = result['facial_areas']['img2']['h']
            boxes = [(x, y, w, h)]

            for (x, y, w, h) in boxes:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)       
            cv2.imshow('Bounding Boxes', image)
            cv2.waitKey(50)
            cv2.destroyAllWindows()
        except ValueError:
            print("unverified")

        if verification_successful: 
            break  # if any verification is successful, stop further verification.

    # Close all windows
    cv2.destroyAllWindows()
    if verification_successful:
        print("Verification successful. Restarting motion detection after 5 seconds")
        time.sleep(5)
    else:
        print("No matches found. Waiting for 5 seconds before restarting motion detection...")
        time.sleep(5)

def detect_motion(frameCount):
    global cap, firstFrame
    motionCounter = 0
    blink_count = 0
    blink_detected = False

    firstFrame = None

    while True:
        ret, frame = cap.read()
        text = "Unoccupied"

        if not ret:
            break

        frame = cv2.resize(frame, (width, width))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gray
            continue

        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            if cv2.contourArea(c) < min_area:
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

            #blink_detected = detect_blink(frame)
            #if blink_detected:
                #print("Blink detected!")
                #blink_count+=1
                #break
            blink_detected = detect_blink(frame)
            if blink_detected:
                print("Blink detected!")
                blink_count+=1
                print(blink_count)
                

            motionCounter += 1
            #print(motionCounter)

            if motionCounter >= frameCount and blink_count >= 7:
                print("Motion detected! Capturing image...")
                capture_image("captured_image.jpg")
                verify_faces("captured_image.jpg", verification_images)
                return  # Return from the function after verification to restart motion detection

        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

if __name__ == "__main__":
    # Initialize the video stream and allow the camera sensor to warmup
    cap = cv2.VideoCapture(0)

    # List of images to verify against
    verification_images = ["unnamed.jpg", "Anand.jpg", "amma.jpg"]

    # Start the motion detection
    while True:
        detect_motion(frame_count)
