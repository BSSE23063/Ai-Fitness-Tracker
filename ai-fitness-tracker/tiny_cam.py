import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

app = FastAPI()

def simple_stream():
    # Try 0 first, if it fails we will try 1
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    
    if not cap.isOpened():
        print("🚨 CAMERA FAILED TO OPEN")
        return

    print("✅ CAMERA OPENED SUCCESSFULLY")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(simple_stream(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    # Running on port 8002 to avoid any conflicts!
    uvicorn.run(app, host="127.0.0.1", port=8002)