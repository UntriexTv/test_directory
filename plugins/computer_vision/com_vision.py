#! /usr/bin/python3
import io
import time

import picamera
import cv2
import requests
import numpy as np

protopath = "MobileNetSSD_deploy.prototxt"
modelpath = "MobileNetSSD_deploy.caffemodel"
detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)
person_counter = 0

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

# Get the picture (low resolution, so it should be quite fast)
# Here you can also specify other parameters (e.g.:rotate the image)
while True:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.capture(stream, format='jpeg')

    # Convert the picture into a numpy array
    buff = np.frombuffer(stream.getvalue(), dtype=np.uint8)

    # Now creates an OpenCV image
    image = cv2.imdecode(buff, 1)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    (H, W) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 0.007843, (W, H), 127.5)

    detector.setInput(blob)
    person_detections = detector.forward()

    for i in np.arange(0, person_detections.shape[2]):
        confidence = person_detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(person_detections[0, 0, i, 1])

            if CLASSES[idx] == "person":
                person_counter += 1

    r = requests.post("http://127.0.0.1:8000/update_sensor", json={"name": "Pocet ludi", "value": str(person_counter)})
    time.sleep(30)
