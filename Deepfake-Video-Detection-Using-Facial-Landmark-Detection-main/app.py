from flask import Flask, request, jsonify
import cv2
import os
import threading
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_faces'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

process_status = []
process_status_lock = threading.Lock()

def safe_append_status(message):
    with process_status_lock:
        process_status.append(message)

@app.route('/upload', methods=['POST'])
def upload_files():
    safe_append_status("Initializing upload process...")
    if 'video' not in request.files or 'image' not in request.files:
        return jsonify({'error': 'Video and image files are required'}), 400
    
    video_file = request.files['video']
    image_file = request.files['image']
    
    unique_video_name = str(uuid.uuid4()) + "_" + video_file.filename
    unique_image_name = str(uuid.uuid4()) + "_" + image_file.filename
    
    video_path = os.path.join(UPLOAD_FOLDER, unique_video_name)
    image_path = os.path.join(UPLOAD_FOLDER, unique_image_name)
    
    video_file.save(video_path)
    image_file.save(image_path)
    
    threading.Thread(target=process_video, args=(video_path,)).start()
    
    return jsonify({'message': 'Files uploaded successfully, processing started.'}), 200

def process_video(video_path):
    safe_append_status("Video processing started.")
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            safe_append_status("Error: Unable to open video file.")
            return
        
        frame_count = 0
        face_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            safe_append_status(f"Processing frame {frame_count}")
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            for (x, y, w, h) in faces:
                face_img = frame[y:y+h, x:x+w]
                face_count += 1
                face_path = os.path.join(PROCESSED_FOLDER, f"face_{frame_count}_{face_count}.jpg")
                cv2.imwrite(face_path, face_img)
                safe_append_status(f"Face saved: {face_path}")
        
        cap.release()
        safe_append_status("Video processing completed.")
    except Exception as e:
        safe_append_status(f"Error during processing: {str(e)}")

@app.route('/process_status', methods=['GET'])
def get_process_status():
    with process_status_lock:
        return jsonify({"status": process_status})

if __name__ == '__main__':
    app.run(debug=True)
