import numpy as np
import time

# ==========================================
# MATH & HELPER FUNCTIONS
# ==========================================
def calculate_angle_3d(a, b, c):
    """Calculates the 3D angle between 3 points using X, Y, and Z coordinates."""
    a, b, c = np.array(a), np.array(b), np.array(c)
    
    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    
    return np.degrees(angle)

def get_landmark_3d(landmarks, landmark_type):
    """Helper to quickly extract [x, y, z] from MediaPipe landmarks."""
    return [
        landmarks[landmark_type.value].x,
        landmarks[landmark_type.value].y,
        landmarks[landmark_type.value].z
    ]

# ==========================================
# EXERCISE TRACKER CLASSES
# ==========================================
class PushupTracker:
    def __init__(self):
        self.counter = 0
        self.stage = "UP"

    def process(self, landmarks, mp_pose):
        shoulder = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
        elbow = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW)
        wrist = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)
        hip = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
        ankle = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)

        elbow_angle = calculate_angle_3d(shoulder, elbow, wrist)
        body_alignment = calculate_angle_3d(shoulder, hip, ankle)

        feedback = "Good Rep!"
        color = (0, 255, 0) # Green

        if body_alignment > 150: 
            if elbow_angle > 150: 
                self.stage = "UP"
                feedback = "Go Lower!"
            if elbow_angle < 85 and self.stage == "UP": 
                self.stage = "DOWN"
                self.counter += 1
        else:
            feedback = "Straighten your back!"
            color = (0, 0, 255) # Red

        return self.counter, self.stage, feedback, color

class SquatTracker:
    def __init__(self):
        self.counter = 0
        self.stage = "UP"

    def process(self, landmarks, mp_pose):
        shoulder = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
        hip = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
        knee = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_KNEE)
        ankle = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)

        knee_angle = calculate_angle_3d(hip, knee, ankle)
        hip_angle = calculate_angle_3d(shoulder, hip, knee)

        feedback = "Good Rep!"
        color = (0, 255, 0)

        # Squat Logic
        if hip_angle > 50: # Ensure they aren't leaning too far forward
            if knee_angle > 160:
                self.stage = "UP"
                feedback = "Squat Down!"
            if knee_angle < 90 and self.stage == "UP":
                self.stage = "DOWN"
                self.counter += 1
        else:
            feedback = "Keep chest up!"
            color = (0, 0, 255)

        return self.counter, self.stage, feedback, color

class PlankTracker:
    def __init__(self):
        self.start_time = None
        self.total_time = 0

    def process(self, landmarks, mp_pose):
        shoulder = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
        hip = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
        ankle = get_landmark_3d(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)

        body_alignment = calculate_angle_3d(shoulder, hip, ankle)
        
        feedback = "Hold it!"
        color = (0, 255, 0)
        stage = "HOLDING"

        # Plank requires a straight back
        if body_alignment > 160:
            if self.start_time is None:
                self.start_time = time.time()
            self.total_time = int(time.time() - self.start_time)
            feedback = f"Great form!"
        else:
            self.start_time = None # Reset timer if form breaks
            stage = "RESTING"
            feedback = "Drop hips / Straighten back!"
            color = (0, 0, 255)

        return self.total_time, stage, feedback, color