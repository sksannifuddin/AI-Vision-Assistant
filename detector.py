"""
YOLO + OpenCV detector.
"""

import cv2
from ultralytics import YOLO

from danger_logic import build_instruction


class VisionDetector:
    def __init__(self, model_path: str = "yolov8n.pt", confidence: float = 0.45):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect_frame(self, frame):
        """Detect objects and return annotated frame, detections, danger level, instruction."""
        results = self.model(frame, conf=self.confidence, verbose=False)
        result = results[0]
        annotated = result.plot()

        detections = []
        names = self.model.names

        if result.boxes is not None:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                label = names[cls_id]
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                detections.append({
                    "label": label,
                    "confidence": round(conf, 2),
                    "box": [x1, y1, x2, y2]
                })

        h, w = frame.shape[:2]
        danger_level, instruction = build_instruction(detections, w, h)

        # Draw screen zones
        cv2.line(annotated, (w // 3, 0), (w // 3, h), (255, 255, 255), 2)
        cv2.line(annotated, (2 * w // 3, 0), (2 * w // 3, h), (255, 255, 255), 2)

        # Draw instruction banner
        color = (0, 200, 0)
        if danger_level == "medium":
            color = (0, 180, 255)
        elif danger_level == "high":
            color = (0, 0, 255)

        cv2.rectangle(annotated, (0, 0), (w, 45), color, -1)
        cv2.putText(annotated, instruction[:95], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        return annotated, detections, danger_level, instruction
