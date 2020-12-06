import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
import time
import threading
import asyncio
from datetime import datetime


def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    """
    encode a face given the file name
    """
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face():
    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    name = "Unknown"
    #img = cv2.imread(im, 1)
    #imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    #img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    #img = img[:,:,::-1]

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
    # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(imgS)
        unknown_face_encodings = face_recognition.face_encodings(imgS, face_locations)
        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            m =face_distances[best_match_index]

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)

            for (y1, x2, y2, x1), name in zip(face_locations, face_names):
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 16, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 0.50, (255, 255, 255), 1)

        markAttendance(name,m)

    # Display the resulting image
        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_names

def markAttendance(name,m):
    f = open('Registro.csv','r+')
    myDataList = f.readlines()
    nameList = []
    event = threading.Event()
    while True:
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        dt_string = time.strftime("%B %d %Y, %H:%M:%S")
        f.writelines(f'\n{name}, {dt_string},{str(round(m,3))}')
        event.wait(1)
        break

#print(classify_face("test.jpg"))
print(classify_face())

