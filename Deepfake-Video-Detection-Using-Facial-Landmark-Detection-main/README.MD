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


