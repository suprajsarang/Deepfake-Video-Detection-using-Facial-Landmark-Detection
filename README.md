# Deepfake Video Detection using Facial Landmark Detection

## 📌 Overview

This project aims to detect deepfake videos in real-time by analyzing facial landmarks. Using **MediaPipe** for landmark extraction and a lightweight classification approach, the system identifies inconsistencies in facial movements and expressions that are typical of deepfake content.

A web-based interface is built using **Flask**, allowing users to upload video files and get results classifying them as either **Authentic** or **Fake**.

---

## 💡 Features

- 🎯 Real-time detection of deepfake videos  
- 🎥 Facial landmark extraction using MediaPipe (468 landmarks)  
- 🔍 Analyzes inconsistencies to classify deepfakes  
- 🌐 Flask-based web interface for video upload and results  
- ⚡ Lightweight and scalable solution

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Framework:** Flask  
- **Computer Vision:** MediaPipe, OpenCV  
- **Frontend:** HTML, CSS  
- **Libraries:** NumPy, cv2

---

## 🧠 How It Works

1. User uploads a video via the web interface  
2. Each frame is processed to extract 468 facial landmarks  
3. The landmarks are analyzed to identify deepfake patterns  
4. The model outputs whether the video is *Authentic* or *Fake*

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/deepfake-detection.git
cd deepfake-detection
pip install -r requirements.txt
python app.py
Visit http://127.0.0.1:5000 and upload your video to test.

deepfake-detection/
├── app.py                # Flask backend
├── templates/
│   └── index.html        # Frontend UI
├── static/
│   └── style.css         # Optional: CSS styling
├── model/                # (Optional) Trained models or configs
├── utils.py              # Landmark extraction & logic
├── requirements.txt
