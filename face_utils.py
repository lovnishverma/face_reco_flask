"""
Face Recognition Utility Module
Handles face encoding, recognition, database management, and webcam streaming.
"""

import os
import pickle
import shutil
from datetime import datetime

import cv2
import face_recognition
import numpy as np
from PIL import Image

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FACES_DIR = os.path.join(BASE_DIR, "known_faces")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "face_db.pkl")
HISTORY_PATH = os.path.join(BASE_DIR, "history.pkl")

# Ensure directories exist
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Recognition tolerance (lower = stricter)
TOLERANCE = 0.5


def _load_db():
    """Load the face encoding database from disk."""
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "rb") as f:
            return pickle.load(f)
    return {"names": [], "encodings": []}


def _save_db(db):
    """Save the face encoding database to disk."""
    with open(DB_PATH, "wb") as f:
        pickle.dump(db, f)


def _load_history():
    """Load recognition history."""
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "rb") as f:
            return pickle.load(f)
    return []


def _save_history(history):
    """Save recognition history."""
    with open(HISTORY_PATH, "wb") as f:
        pickle.dump(history, f)


def register_face(image_path, name):
    """
    Register a new face.
    Returns: (success: bool, message: str)
    """
    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            return False, "No face detected in the image. Please upload a clear photo with a visible face."

        if len(encodings) > 1:
            return False, "Multiple faces detected. Please upload a photo with only one face."

        encoding = encodings[0]

        # Save the image to known_faces directory
        person_dir = os.path.join(KNOWN_FACES_DIR, name)
        os.makedirs(person_dir, exist_ok=True)

        # Save a copy of the image
        img = Image.open(image_path)
        img.thumbnail((400, 400))
        save_path = os.path.join(person_dir, "face.jpg")
        img.save(save_path, "JPEG", quality=90)

        # Update database
        db = _load_db()
        # Remove old encoding for this person if exists
        indices = [i for i, n in enumerate(db["names"]) if n == name]
        for i in sorted(indices, reverse=True):
            db["names"].pop(i)
            db["encodings"].pop(i)

        db["names"].append(name)
        db["encodings"].append(encoding)
        _save_db(db)

        return True, f"Successfully registered '{name}'!"

    except Exception as e:
        return False, f"Error processing image: {str(e)}"


def recognize_faces(image_path):
    """
    Recognize faces in an image.
    Returns: (annotated_image_path, results: list of dicts)
    """
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    db = _load_db()
    results = []

    # Convert to BGR for OpenCV drawing
    img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        confidence = 0.0

        if len(db["encodings"]) > 0:
            distances = face_recognition.face_distance(db["encodings"], encoding)
            best_idx = np.argmin(distances)
            best_distance = distances[best_idx]

            if best_distance <= TOLERANCE:
                name = db["names"][best_idx]
                confidence = round((1 - best_distance) * 100, 1)

        results.append({
            "name": name,
            "confidence": confidence,
            "location": {"top": top, "right": right, "bottom": bottom, "left": left}
        })

        # Draw bounding box
        color = (0, 230, 118) if name != "Unknown" else (0, 100, 255)
        cv2.rectangle(img_bgr, (left, top), (right, bottom), color, 2)

        # Draw label background
        label = f"{name} ({confidence}%)" if name != "Unknown" else "Unknown"
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        cv2.rectangle(img_bgr, (left, bottom), (left + label_size[0] + 10, bottom + label_size[1] + 16), color, -1)
        cv2.putText(img_bgr, label, (left + 5, bottom + label_size[1] + 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Save annotated image
    result_path = os.path.join(UPLOADS_DIR, "result_" + os.path.basename(image_path))
    cv2.imwrite(result_path, img_bgr)

    # Log to history
    history = _load_history()
    history.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "faces_found": len(results),
        "recognized": [r["name"] for r in results if r["name"] != "Unknown"],
        "unknown_count": sum(1 for r in results if r["name"] == "Unknown")
    })
    # Keep last 50 entries
    history = history[:50]
    _save_history(history)

    return result_path, results


def get_all_registered():
    """Get all registered people with their info."""
    db = _load_db()
    people = {}

    for name in set(db["names"]):
        person_dir = os.path.join(KNOWN_FACES_DIR, name)
        photo_path = os.path.join(person_dir, "face.jpg")
        has_photo = os.path.exists(photo_path)
        count = db["names"].count(name)

        people[name] = {
            "name": name,
            "photo": f"/known_face_photo/{name}" if has_photo else None,
            "encoding_count": count
        }

    return people


def delete_person(name):
    """Delete a registered person from the database."""
    db = _load_db()

    indices = [i for i, n in enumerate(db["names"]) if n == name]
    if not indices:
        return False, f"Person '{name}' not found."

    for i in sorted(indices, reverse=True):
        db["names"].pop(i)
        db["encodings"].pop(i)

    _save_db(db)

    # Remove their photos
    person_dir = os.path.join(KNOWN_FACES_DIR, name)
    if os.path.exists(person_dir):
        shutil.rmtree(person_dir)

    return True, f"Successfully deleted '{name}'."


def get_stats():
    """Get dashboard statistics."""
    db = _load_db()
    history = _load_history()

    total_people = len(set(db["names"]))
    total_recognitions = len(history)
    recent = history[:5]

    return {
        "total_people": total_people,
        "total_recognitions": total_recognitions,
        "recent_history": recent
    }


def generate_frames():
    """Generator function for webcam streaming with face recognition."""
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        return

    db = _load_db()
    known_encodings = db["encodings"]
    known_names = db["names"]

    frame_count = 0
    face_locations = []
    face_names = []
    face_confidences = []

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break

            # Process every 3rd frame for performance
            if frame_count % 3 == 0:
                # Resize for faster processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small)
                face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

                face_names = []
                face_confidences = []

                for encoding in face_encodings:
                    name = "Unknown"
                    confidence = 0.0

                    if len(known_encodings) > 0:
                        distances = face_recognition.face_distance(known_encodings, encoding)
                        best_idx = np.argmin(distances)
                        best_distance = distances[best_idx]

                        if best_distance <= TOLERANCE:
                            name = known_names[best_idx]
                            confidence = round((1 - best_distance) * 100, 1)

                    face_names.append(name)
                    face_confidences.append(confidence)

            frame_count += 1

            # Draw annotations on full-size frame
            for (top, right, bottom, left), name, conf in zip(face_locations, face_names, face_confidences):
                # Scale back up
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                color = (0, 230, 118) if name != "Unknown" else (0, 100, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                label = f"{name} ({conf}%)" if name != "Unknown" else "Unknown"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                cv2.rectangle(frame, (left, bottom), (left + label_size[0] + 10, bottom + label_size[1] + 20), color, -1)
                cv2.putText(frame, label, (left + 5, bottom + label_size[1] + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    finally:
        camera.release()
