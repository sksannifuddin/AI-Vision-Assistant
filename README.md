# AI Vision Assistant for Blind People

A real-time AI assistive vision web app that uses a laptop webcam or phone IP camera to detect people, vehicles, and obstacles, then speaks navigation guidance in multiple languages.

## Main Features

- Real-time webcam object detection
- YOLO-based object recognition
- Voice guidance for blind/visually impaired users
- Multilingual support: English, Telugu, Hindi, Marathi, Gujarati, Tamil, Kannada, Malayalam, Bengali, Urdu, Arabic, French, Spanish, German, Chinese, Japanese, Korean, and more
- Danger-level detection: safe, low, medium, high
- Direction guidance: go straight, move left, move right, stop
- Flask web dashboard with live camera feed
- Detection logs saved in `logs/detections.jsonl`
- Phone camera support using IP webcam URL

## Tech Stack

- Python
- Flask
- OpenCV
- Ultralytics YOLO
- pyttsx3
- gTTS
- googletrans
- HTML, CSS, JavaScript

## How to Run

### 1. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install packages

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

## Important Notes

The first run may download the YOLO model file automatically.

Offline voice works without internet, but may mainly speak in English depending on your system voices.

For proper multilingual voice, choose **Online Multilingual Voice** in the web app. It needs internet.

## Use Phone Camera

Install any IP Webcam app on your phone. Start camera server, then copy the video URL.

Example:

```bash
export CAMERA_URL="http://192.168.1.5:8080/video"
python app.py
```

On Windows PowerShell:

```powershell
$env:CAMERA_URL="http://192.168.1.5:8080/video"
python app.py
```

## Final-Year Project Title

**AI-Powered Multilingual Vision Assistant for Visually Impaired People**

## Resume Description

Built a real-time AI vision assistant using Python, Flask, OpenCV, YOLO, and multilingual text-to-speech to help visually impaired users detect obstacles, people, and vehicles from live camera input. The system provides spoken safety alerts, danger-level classification, and directional guidance in multiple languages.

## Future Scope

- Train custom model for potholes, manholes, stairs, open drainage, zebra crossings
- Add GPS-based navigation
- Add emergency contact alert
- Add smart glasses hardware integration
- Add vibration feedback module
- Add Android app
- Add MongoDB dashboard for journey history
