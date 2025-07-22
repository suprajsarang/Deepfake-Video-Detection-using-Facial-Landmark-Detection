import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

real_image_path = "Deepfake_video_detection-main/utils/image.png"
real_image = cv2.imread(real_image_path)
real_landmarks = []

def extract_landmarks(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    if results.multi_face_landmarks:
        landmarks = [(lm.x, lm.y) for lm in results.multi_face_landmarks[0].landmark]
        return np.array(landmarks)
    return None

real_landmarks = extract_landmarks(real_image)

def calculate_similarity(landmarks1, landmarks2):
    if landmarks1 is None or landmarks2 is None:
        return np.nan
    distances = np.linalg.norm(landmarks1 - landmarks2, axis=1)
    return np.mean(distances)

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    similarities_to_real = []
    similarities_to_prev = []
    prev_landmarks = None

    frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Retrieve frame rate once
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Optional: Resize for higher resolution
        frame_resized = cv2.resize(frame, (frame.shape[1], frame.shape[0]))

        # Extract landmarks
        landmarks = extract_landmarks(frame_resized)

        # Similarity calculations
        sim_to_real = calculate_similarity(landmarks, real_landmarks)
        similarities_to_real.append(sim_to_real)

        if prev_landmarks is not None:
            sim_to_prev = calculate_similarity(landmarks, prev_landmarks)
            similarities_to_prev.append(sim_to_prev)
        else:
            similarities_to_prev.append(np.nan)  # No similarity for the first frame

        prev_landmarks = landmarks
        frame_count += 1

    cap.release()

    # Filter out NaN values
    similarities_to_real_clean = [x for x in similarities_to_real if not np.isnan(x)]
    similarities_to_prev_clean = [x for x in similarities_to_prev if not np.isnan(x)]

    print("Similarities to Real:", similarities_to_real_clean)
    print("Similarities to Previous:", similarities_to_prev_clean)

    # Plot similarities
    plt.figure(figsize=(10, 5))
    plt.plot(similarities_to_real, label="Similarity to Real Image", color="blue")
    plt.plot(similarities_to_prev, label="Similarity to Previous Frame", color="red")
    plt.xlabel("Frame Index")
    plt.ylabel("Similarity Score")
    plt.title(f"Similarity Scores Across Frames (Avg FPS: {frame_rate:.2f})")
    plt.legend()
    plt.savefig("output_plot.png")
    plt.show()

    print(f"Average Frame Rate: {frame_rate:.2f} fps")
    print(f"Processed {frame_count} frames.")

process_video("Deepfake_video_detection-main/utils/fake.mp4")
