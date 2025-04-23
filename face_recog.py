import face_recognition
import numpy as np
import cv2
import pickle

# 学習済みの顔エンコーディングと名前の読み込み
with open('models/known_faces.pkl', 'rb') as f:
    known_encodings, known_names = pickle.load(f)

def is_authenticated_and_get_name(image):
    if image is None:
        print("❌ 入力画像がNone")
        return False, None

    # OpenCVの画像はBGRなのでRGBに変換（face_recognitionがRGBを要求）
    small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # 顔検出
    face_locations = face_recognition.face_locations(rgb_frame)
    if len(face_locations) == 0:
        print("❌ 顔が検出されませんでした")
        return False, None

    # 顔特徴量抽出
    try:
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    except Exception as e:
        print(f"⚠️ face_encodings エラー: {e}")
        return False, None

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding)
        face_distances = face_recognition.face_distance(known_encodings, encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            return True, known_names[best_match_index]

    return False, None