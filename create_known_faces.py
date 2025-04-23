# create_known_faces.py
import face_recognition
import pickle
import os

known_encodings = []
known_names = []

for filename in os.listdir("known_faces"):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        name = os.path.splitext(filename)[0]
        image = face_recognition.load_image_file(os.path.join("known_faces", filename))
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(name)

with open("models/known_faces.pkl", "wb") as f:
    pickle.dump((known_encodings, known_names), f)