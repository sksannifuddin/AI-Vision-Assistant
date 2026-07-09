from datetime import datetime
import json
import os

import cv2
from flask import Flask, Response, jsonify, render_template, request

from detector import VisionDetector
from voice import LANGUAGES, speak_alert

app = Flask(__name__)

# Global app state
camera = None
detector = VisionDetector(model_path=os.getenv("YOLO_MODEL", "yolov8n.pt"))
current_language = "english"
voice_mode = "offline"  # offline or online
voice_enabled = True
last_status = {
    "danger_level": "safe",
    "instruction": "System ready.",
    "translated_instruction": "System ready.",
    "detections": [],
    "time": ""
}

LOG_FILE = "logs/detections.jsonl"
os.makedirs("logs", exist_ok=True)


def get_camera_source():
    """
    Default: laptop webcam 0.
    For phone IP camera, set CAMERA_URL env variable, for example:
    export CAMERA_URL="http://192.168.1.5:8080/video"
    """
    return os.getenv("CAMERA_URL", "0")


def open_camera():
    global camera
    source = get_camera_source()
    source = int(source) if str(source).isdigit() else source
    camera = cv2.VideoCapture(source)
    return camera


def save_log(payload: dict):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def generate_frames():
    global camera, last_status

    if camera is None or not camera.isOpened():
        open_camera()

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        annotated, detections, danger_level, instruction = detector.detect_frame(frame)

        translated_instruction = instruction
        if voice_enabled:
            translated_instruction = speak_alert(
                instruction,
                language_name=current_language,
                mode=voice_mode,
                cooldown=4
            )

        last_status = {
            "danger_level": danger_level,
            "instruction": instruction,
            "translated_instruction": translated_instruction,
            "detections": detections[:10],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if danger_level in {"medium", "high"}:
            save_log(last_status)

        ok, buffer = cv2.imencode(".jpg", annotated)
        if not ok:
            continue

        frame_bytes = buffer.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )


@app.route("/")
def index():
    return render_template("index.html", languages=sorted(LANGUAGES.keys()))


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/status")
def status():
    return jsonify(last_status)


@app.route("/settings", methods=["POST"])
def settings():
    global current_language, voice_mode, voice_enabled

    data = request.get_json(force=True)
    current_language = data.get("language", current_language).lower()
    voice_mode = data.get("voice_mode", voice_mode).lower()
    voice_enabled = bool(data.get("voice_enabled", voice_enabled))

    return jsonify({
        "message": "Settings updated",
        "language": current_language,
        "voice_mode": voice_mode,
        "voice_enabled": voice_enabled
    })


@app.route("/test_voice", methods=["POST"])
def test_voice():
    data = request.get_json(force=True)
    language = data.get("language", current_language)
    mode = data.get("voice_mode", voice_mode)
    text = "Voice guidance is active. Path is clear. Go straight."
    translated = speak_alert(text, language_name=language, mode=mode, cooldown=0)
    return jsonify({"spoken": translated})


@app.route("/stop_camera", methods=["POST"])
def stop_camera():
    global camera
    if camera is not None:
        camera.release()
        camera = None
    return jsonify({"message": "Camera stopped"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
