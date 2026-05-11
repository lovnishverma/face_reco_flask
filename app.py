"""
Face Recognition Web Application
Flask server with routes for face registration, recognition, webcam streaming, and database management.
"""

import os

from flask import (Flask, Response, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename

from face_utils import (delete_person, generate_frames, get_all_registered,
                        get_stats, recognize_faces, register_face)

app = Flask(__name__)
app.secret_key = "face_reco_secret_key_2026"

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
KNOWN_FACES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "known_faces")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── Routes ────────────────────────────────────────────────────


@app.route("/")
def index():
    """Dashboard page."""
    stats = get_stats()
    return render_template("index.html", stats=stats)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new face."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        file = request.files.get("photo")

        if not name:
            flash("Please enter a name.", "error")
            return redirect(url_for("register"))

        if not file or file.filename == "":
            flash("Please select a photo.", "error")
            return redirect(url_for("register"))

        if not allowed_file(file.filename):
            flash("Invalid file type. Please upload a JPG, PNG, or WebP image.", "error")
            return redirect(url_for("register"))

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        success, message = register_face(filepath, name)

        # Cleanup uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

        if success:
            flash(message, "success")
        else:
            flash(message, "error")

        return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/recognize", methods=["GET", "POST"])
def recognize():
    """Recognize faces in an uploaded image."""
    results = None
    result_image = None

    if request.method == "POST":
        file = request.files.get("photo")

        if not file or file.filename == "":
            flash("Please select a photo.", "error")
            return redirect(url_for("recognize"))

        if not allowed_file(file.filename):
            flash("Invalid file type. Please upload a JPG, PNG, or WebP image.", "error")
            return redirect(url_for("recognize"))

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        result_path, results = recognize_faces(filepath)
        result_image = os.path.basename(result_path)

        # Cleanup original upload
        if os.path.exists(filepath):
            os.remove(filepath)

    return render_template("recognize.html", results=results, result_image=result_image)


@app.route("/webcam")
def webcam():
    """Live webcam recognition page."""
    return render_template("webcam.html")


@app.route("/video_feed")
def video_feed():
    """Video streaming route for webcam feed."""
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/database")
def database():
    """View and manage registered faces."""
    people = get_all_registered()
    return render_template("database.html", people=people)


@app.route("/delete/<name>", methods=["POST"])
def delete(name):
    """Delete a registered person."""
    success, message = delete_person(name)
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    return redirect(url_for("database"))


# ─── Static file serving ──────────────────────────────────────


@app.route("/known_face_photo/<name>")
def known_face_photo(name):
    """Serve registered face photos."""
    person_dir = os.path.join(KNOWN_FACES_DIR, secure_filename(name))
    return send_from_directory(person_dir, "face.jpg")


@app.route("/result_image/<filename>")
def result_image(filename):
    """Serve recognition result images."""
    return send_from_directory(UPLOAD_FOLDER, filename)


# ─── Run ──────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
