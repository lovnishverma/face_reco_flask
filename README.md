# 🔐 FaceVault — Face Recognition Web App

A complete face recognition system built with **Flask** and **Python**, featuring face registration, image-based recognition, real-time webcam detection, and a face database manager — all wrapped in a stunning dark glassmorphism UI.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?logo=flask)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## ✨ Features

| Feature | Description |
|---|---|
| 👤 **Register Face** | Upload a photo + name to register a person in the database |
| 🔍 **Recognize from Upload** | Upload any image to identify all faces with confidence scores |
| 📹 **Live Webcam Recognition** | Real-time face detection & recognition via webcam stream |
| 🗃️ **Face Database** | View, search, and delete registered faces |
| 📊 **Dashboard** | Stats overview, quick actions, and recent activity feed |
| 📜 **Recognition History** | Logs of past scans with timestamps |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Flask (Python) |
| **Face Detection** | OpenCV + face\_recognition (dlib) |
| **Face Encoding** | 128-dimensional face vectors via dlib |
| **Face Matching** | Euclidean distance comparison (tolerance: 0.5) |
| **Storage** | Pickle database + filesystem for images |
| **Frontend** | Jinja2 templates, vanilla CSS & JS |
| **UI Theme** | Dark mode with glassmorphism design |

---

## 📁 Project Structure

```
face_reco/
├── app.py                  # Flask server + all routes
├── face_utils.py           # Face encoding, recognition & webcam engine
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── known_faces/            # Stored face images (auto-created)
├── uploads/                # Temporary uploads (auto-created)
├── face_db.pkl             # Face encodings database (auto-created)
├── history.pkl             # Recognition history (auto-created)
├── static/
│   ├── css/
│   │   └── style.css       # Premium dark glassmorphism stylesheet
│   └── js/
│       └── app.js          # Drag-and-drop, preview, animations
└── templates/
    ├── base.html           # Base layout with sidebar navigation
    ├── index.html          # Dashboard page
    ├── register.html       # Face registration page
    ├── recognize.html      # Image upload recognition page
    ├── webcam.html         # Live webcam recognition page
    └── database.html       # Face database management page
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9 – 3.13** (Windows supported)
- **pip** (Python package manager)
- A **webcam** (optional, for live recognition)

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd face_reco
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** This project uses a [precompiled face\_recognition build](https://github.com/lovnishverma/face_recognition) that bundles a prebuilt `dlib` wheel — no CMake or Visual Studio Build Tools needed on Windows!

4. **Run the application**

   ```bash
   python app.py
   ```

5. **Open in browser**

   ```
   http://127.0.0.1:5000
   ```

---

## 📖 Usage Guide

### 1. Register a Face

- Navigate to **Register Face** from the sidebar
- Enter the person's name
- Upload a clear, front-facing photo (one face per image)
- Click **Register Face**

### 2. Recognize Faces from an Image

- Navigate to **Recognize** from the sidebar
- Upload any image (can contain multiple faces)
- The system will annotate recognized faces with names and confidence scores

### 3. Live Webcam Recognition

- Navigate to **Live Webcam** from the sidebar
- Click **Start Camera**
- Recognized faces appear with green bounding boxes and names
- Unknown faces appear with orange bounding boxes

### 4. Manage Database

- Navigate to **Database** from the sidebar
- Search registered faces by name
- Delete a person with the delete button (with confirmation)

---

## ⚙️ Configuration

Key settings in `face_utils.py`:

| Setting | Default | Description |
|---|---|---|
| `TOLERANCE` | `0.5` | Face match threshold (lower = stricter, range: 0.0–1.0) |
| Max upload size | `16 MB` | Configured in `app.py` via `MAX_CONTENT_LENGTH` |
| Webcam frame skip | `3` | Processes every 3rd frame for performance |
| Webcam resize factor | `0.25` | Downscales webcam input for faster processing |
| History limit | `50` | Number of recent recognition logs kept |

---

## 🔑 API Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Dashboard with stats and recent activity |
| `GET/POST` | `/register` | Register a new face |
| `GET/POST` | `/recognize` | Upload and recognize faces |
| `GET` | `/webcam` | Live webcam recognition page |
| `GET` | `/video_feed` | MJPEG video stream endpoint |
| `GET` | `/database` | View registered faces |
| `POST` | `/delete/<name>` | Delete a registered person |
| `GET` | `/known_face_photo/<name>` | Serve registered face photo |
| `GET` | `/result_image/<filename>` | Serve recognition result image |

---

## 📸 Tips for Best Results

- Use **clear, well-lit photos** for registration
- Face should be **front-facing** and clearly visible
- Avoid **sunglasses** or heavy face coverings
- Register with **one person per photo**
- For webcam: ensure good lighting for accurate real-time detection

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [face\_recognition](https://github.com/lovnishverma/face_recognition) — Precompiled build with bundled dlib wheel
- [Flask](https://flask.palletsprojects.com/) — Lightweight Python web framework
- [OpenCV](https://opencv.org/) — Computer vision library
- [dlib](http://dlib.net/) — Machine learning toolkit for face encoding

---

<p align="center">
  Built with ❤️ using Flask & Python
</p>
