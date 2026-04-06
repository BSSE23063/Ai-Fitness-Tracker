from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse # NEW IMPORT
import cv2
import mediapipe as mp
import threading
import time # NEW IMPORT

from trackers import PushupTracker, SquatTracker, PlankTracker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mp_pose = mp.solutions.pose

# =========================
# GLOBAL STATE
# =========================
tracker = None
current_exercise = None
is_running = False
global_frame = None # NEW: Stores the current camera frame for the web!
result = {
    "reps": 0,
    "exercise": None
}

# =========================
# BACKGROUND TRACKING
# =========================
# =========================
# BACKGROUND TRACKING
# =========================
def run_tracking():
    global tracker, is_running, result, global_frame

    # 1. We know this works now! Use CAP_DSHOW
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("🚨 ERROR: Camera failed to open in main app!")
        is_running = False
        return
        
    print("✅ SUCCESS: AI Tracking Started!")
    count = 0
    mp_drawing = mp.solutions.drawing_utils

    with mp_pose.Pose(min_detection_confidence=0.7) as pose:
        while is_running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks and tracker:
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                
                landmarks = results.pose_landmarks.landmark
                count, stage, feedback, color = tracker.process(landmarks, mp_pose)
                
                cv2.putText(image, f"Reps/Time: {count}", (20, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(image, feedback, (20, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            ret, buffer = cv2.imencode('.jpg', image)
            global_frame = buffer.tobytes()

        cap.release()

    result["reps"] = count
    result["exercise"] = current_exercise
    is_running = False
    global_frame = None 

# =========================
# VIDEO STREAMING LOGIC
# =========================
def generate_frames():
    global global_frame, is_running
    
    # 2. Keep the connection alive! Wait patiently for the camera to warm up.
    while True:
        if is_running and global_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n')
            time.sleep(0.03)
        else:
            # If the workout hasn't started yet, just wait. Don't disconnect!
            time.sleep(0.1)

@app.get("/video_feed")
def video_feed():
    # This endpoint streams the frames to React
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


# =========================
# YOUR EXISTING ENDPOINTS
# =========================
@app.get("/")
def home():
    return {"message": "AI Service Running"}

@app.post("/start")
def start_exercise(data: dict):
    global tracker, current_exercise, is_running, global_frame

    if is_running:
        return {"error": "Already running"}

    # Get the exercise name from React and ensure it's lowercase
    exercise = data.get("exercise", "").lower()

    # Look for keywords instead of exact matches!
    if "push" in exercise:
        tracker = PushupTracker()
        current_exercise = "pushups" # Standardize the name
    elif "squat" in exercise:
        tracker = SquatTracker()
        current_exercise = "squats"
    elif "plank" in exercise:
        tracker = PlankTracker()
        current_exercise = "planks"
    else:
        # If it fails, print it out so we can see what React sent!
        print(f"🚨 FAILED TO START: Unknown exercise sent from React: '{exercise}'")
        return {"error": f"Invalid exercise: {exercise}"}

    is_running = True
    global_frame = None # Reset frame

    # THIS will now finally run!
    threading.Thread(target=run_tracking).start()
    return {"message": f"{current_exercise} tracking started"}

@app.post("/stop")
def stop_tracking():
    global is_running
    is_running = False
    return {"message": "Tracking stopped"}

@app.get("/result")
def get_result():
    return result