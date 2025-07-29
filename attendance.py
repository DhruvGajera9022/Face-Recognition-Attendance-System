import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
from win32com.client import Dispatch

DATA_DIR = 'data'
ATTENDANCE_DIR = 'Attendance'
HAAR_CASCADE_PATH = os.path.join(DATA_DIR, 'haarcascade_frontalface_default.xml')
FACE_DATA_PATH = os.path.join(DATA_DIR, 'faces_data.pkl')
NAME_DATA_PATH = os.path.join(DATA_DIR, 'names.pkl')
IMAGE_SIZE = (50, 50)

def speak(message):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(message)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_training_data():
    with open(NAME_DATA_PATH, 'rb') as name_file, open(FACE_DATA_PATH, 'rb') as face_file:
        names = pickle.load(name_file)
        faces = pickle.load(face_file)
    return faces, names

def mark_attendance(name):
    ts = time.time()
    date_str = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    time_str = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
    filename = os.path.join(ATTENDANCE_DIR, f"Attendance_{date_str}.csv")

    ensure_dir(ATTENDANCE_DIR)

    attendance = [name, time_str]

    already_marked = False
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing = f.readlines()
            already_marked = any(name in line for line in existing)

    if not already_marked:
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if os.path.getsize(filename) == 0:
                writer.writerow(['NAME', 'TIME'])
            writer.writerow(attendance)
        speak(f"Attendance taken for {name}")
    else:
        speak(f"Already marked for {name}")

def main():
    ensure_dir(DATA_DIR)
    if not os.path.exists(HAAR_CASCADE_PATH):
        print(f"❌ Haar cascade not found at {HAAR_CASCADE_PATH}")
        return

    try:
        faces_data, labels = load_training_data()
    except Exception as e:
        print("❌ Failed to load face data:", e)
        return

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces_data, labels)

    face_detect = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    video = cv2.VideoCapture(0)

    print("📷 Press 'o' to mark attendance, 'q' to quit.")

    while True:
        ret, frame = video.read()
        if not ret:
            print("⚠️ Frame not read properly.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_crop = frame[y:y+h, x:x+w]
            face_resized = cv2.resize(face_crop, IMAGE_SIZE).flatten().reshape(1, -1)
            output = knn.predict(face_resized)
            name = output[0]

            # Drawing on frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, name, (x + 5, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            recognized_name = name  # Capture for attendance

        cv2.imshow("Face Recognition", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('o') and 'recognized_name' in locals():
            mark_attendance(recognized_name)
            time.sleep(2)

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
