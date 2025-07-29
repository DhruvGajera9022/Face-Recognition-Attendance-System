import cv2
import pickle
import numpy as np
import os

DATA_DIR = 'data'
FACE_DATA_FILE = os.path.join(DATA_DIR, 'faces_data.pkl')
NAME_DATA_FILE = os.path.join(DATA_DIR, 'names.pkl')
FACE_CASCADE_PATH = os.path.join(DATA_DIR, 'haarcascade_frontalface_default.xml')

MAX_SAMPLES = 100
IMAGE_SIZE = (50, 50)

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_pickle(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None

def save_pickle(obj, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

def main():
    ensure_data_dir()
    name = input("Enter your name: ").strip()
    if not name:
        print("❌ Name cannot be empty.")
        return

    if not os.path.exists(FACE_CASCADE_PATH):
        print(f"❌ Haarcascade file not found at: {FACE_CASCADE_PATH}")
        return

    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print("❌ Cannot access the webcam.")
        return

    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    faces_data = []
    sample_count = 0
    frame_count = 0

    print("📷 Capturing face data. Press 'q' to quit early.")

    while True:
        ret, frame = video.read()
        if not ret:
            print("⚠️ Failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_crop = frame[y:y+h, x:x+w]
            face_resized = cv2.resize(face_crop, IMAGE_SIZE)

            if sample_count < MAX_SAMPLES and frame_count % 10 == 0:
                faces_data.append(face_resized)
                sample_count += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f'Samples: {sample_count}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        frame_count += 1
        cv2.imshow('Face Capture', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or sample_count >= MAX_SAMPLES:
            break

    video.release()
    cv2.destroyAllWindows()

    if sample_count == 0:
        print("❌ No face data collected.")
        return

    faces_data = np.asarray(faces_data).reshape(sample_count, -1)
    names = [name] * sample_count

    # Load and append to existing data if available
    existing_faces = load_pickle(FACE_DATA_FILE)
    existing_names = load_pickle(NAME_DATA_FILE)

    if existing_faces is not None and existing_names is not None:
        faces_data = np.append(existing_faces, faces_data, axis=0)
        names = existing_names + names

    # Save updated data
    save_pickle(faces_data, FACE_DATA_FILE)
    save_pickle(names, NAME_DATA_FILE)

    print(f"✅ Saved {sample_count} face samples for '{name}'.")

if __name__ == '__main__':
    main()
