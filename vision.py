# ai_rover_simulation/vision.py

import cv2
import numpy as np

def detect_features(frame, rover_x, rover_y):
    detections = []

    # Define regions of interest (ROI) near the rover
    roi_size = 60
    x1, y1 = int(rover_x - roi_size), int(rover_y - roi_size)
    x2, y2 = int(rover_x + roi_size), int(rover_y + roi_size)

    roi = frame[max(0, y1):min(y2, frame.shape[0]), max(0, x1):min(x2, frame.shape[1])]

    # Convert to HSV for better color segmentation
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define masks for different features (example values)
    masks = {
        'rock': cv2.inRange(hsv, (5, 50, 50), (15, 255, 255)),         # Orange/Brown
        'ice': cv2.inRange(hsv, (90, 20, 180), (130, 255, 255)),       # Light Blue
        'crater': cv2.inRange(hsv, (0, 0, 0), (180, 255, 40)),         # Very dark
    }

    for label, mask in masks.items():
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) > 30:
                M = cv2.moments(cnt)
                if M['m00'] == 0:
                    continue
                cx = int(M['m10'] / M['m00']) + max(0, x1)
                cy = int(M['m01'] / M['m00']) + max(0, y1)
                detections.append((cx, cy, label))
                cv2.drawContours(frame, [cnt + [max(0, x1), max(0, y1)]], -1, (0, 255, 0), 1)

    return detections
