"""
Danger and navigation logic for AI Vision Assistant.
This file converts raw YOLO detections into simple safety instructions.
"""

DANGEROUS_OBJECTS = {
    "car", "bus", "truck", "motorcycle", "bicycle", "train"
}

OBSTACLE_OBJECTS = {
    "person", "chair", "bench", "backpack", "suitcase", "dog", "cat",
    "car", "bus", "truck", "motorcycle", "bicycle", "traffic light",
    "stop sign", "fire hydrant", "potted plant", "dining table"
}


def get_zone(x_center: float, frame_width: int) -> str:
    """Return LEFT, CENTER, or RIGHT based on object's x-center."""
    left_limit = frame_width / 3
    right_limit = 2 * frame_width / 3

    if x_center < left_limit:
        return "left"
    if x_center > right_limit:
        return "right"
    return "center"


def estimate_distance_level(box_area: float, frame_area: float) -> str:
    """
    Approximate distance using bounding-box size.
    Bigger box usually means object is closer.
    """
    ratio = box_area / frame_area

    if ratio > 0.28:
        return "very close"
    if ratio > 0.13:
        return "close"
    if ratio > 0.05:
        return "medium distance"
    return "far"


def build_instruction(detections: list, frame_width: int, frame_height: int) -> tuple[str, str]:
    """
    Create one spoken instruction from detections.
    Returns: (danger_level, instruction)
    """
    if not detections:
        return "safe", "Path is clear. Go straight."

    frame_area = frame_width * frame_height
    important = []

    for det in detections:
        label = det["label"].lower()
        if label not in OBSTACLE_OBJECTS and label not in DANGEROUS_OBJECTS:
            continue

        x1, y1, x2, y2 = det["box"]
        box_area = max(1, (x2 - x1) * (y2 - y1))
        x_center = (x1 + x2) / 2
        zone = get_zone(x_center, frame_width)
        distance = estimate_distance_level(box_area, frame_area)

        score = box_area
        if label in DANGEROUS_OBJECTS:
            score *= 2
        if zone == "center":
            score *= 2

        important.append({
            "label": label,
            "zone": zone,
            "distance": distance,
            "score": score
        })

    if not important:
        return "safe", "Path is clear. Go straight."

    target = sorted(important, key=lambda x: x["score"], reverse=True)[0]
    label = target["label"]
    zone = target["zone"]
    distance = target["distance"]

    if label in DANGEROUS_OBJECTS:
        if zone == "center" and distance in {"very close", "close"}:
            return "high", f"Warning. {label} is {distance} in front of you. Stop and move carefully."
        return "medium", f"{label} detected on your {zone}. Maintain safe distance."

    if zone == "center":
        if distance in {"very close", "close"}:
            return "high", f"{label} is {distance} in front of you. Stop. Move left or right."
        return "medium", f"{label} ahead. Slow down and go carefully."

    if zone == "left":
        return "low", f"{label} detected on your left. Keep slightly right."

    return "low", f"{label} detected on your right. Keep slightly left."
