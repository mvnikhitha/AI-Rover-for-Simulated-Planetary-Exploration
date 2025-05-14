import cv2
import numpy as np
from rover import Rover
from vision import detect_features

img = cv2.imread("terrain_map.png")
terrain = cv2.resize(img, (600, 600))

terrain = cv2.convertScaleAbs(terrain, alpha=1.2, beta=-30) 
map_height, map_width, _ = terrain.shape
rover = Rover(x=50, y=50, angle=0, map_shape=(map_height, map_width), terrain=terrain)

while True:
    frame = terrain.copy()

    # Move and draw rover
    rover.autonomous_move()
    rover.draw(frame)

    # Detect features
    detected = detect_features(frame, rover.x, rover.y)
    for (cx, cy, label) in detected:
        cv2.putText(frame, label, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    # Display
    cv2.imshow("AI Rover Simulation", frame)
    key = cv2.waitKey(50)

    if key == ord('q'):
        break

cv2.destroyAllWindows()
