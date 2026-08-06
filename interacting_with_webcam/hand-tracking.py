"""
MediaPipe runs a small neural network on each frame and returns 21
LANDMARKS per hand - a point for each joint:

        8   12  16  20        <- fingertips
        |   |   |   |
        7   11  15  19
        |   |   |   |
        6   10  14  18        <- PIP joints (middle knuckle)
        |   |   |   |
    4   5   9   13  17        <- MCP joints (base knuckle)
     \  |  /   /   /
      \ | /   /   /
        0                     <- wrist

    Thumb : 1  2  3  4        (4 = tip)
    Index : 5  6  7  8        (8 = tip)
    Middle: 9  10 11 12       (12 = tip)
    Ring  : 13 14 15 16       (16 = tip)
    Pinky : 17 18 19 20       (20 = tip)

Each landmark has .x, .y, .z as values from 0.0 to 1.0 - they are
NORMALISED to the frame size. To get pixels, multiply by width/height.
This is deliberate: the same code works at any resolution.

The important idea for today: once you have those 21 numbers, the neural
network's job is DONE. Everything after that is ordinary geometry that
you can write yourself. That is what Block 4 is about.

HOW TO RUN
----------
    python 03_hand_tracking.py

Keys:  1  skeleton view
       2  fingertip only
       3  pinch distance
       q  quit
"""

import cv2
import numpy as np
import mediapipe as mp
from camera_utils import open_camera, read_frame, cleanup

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

def to_pixels(landmark, frame_shape):
    """Convert a normalised landmark (0..1) into integer (x, y) pixels."""
    h, w = frame_shape[:2]
    return int(landmark.x * w), int(landmark.y * h)

def view_skeleton(frame, hand_landmarks):
    mp_draw.draw_landmarks(
        frame,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_styles.get_default_hand_landmarks_style(),
        mp_styles.get_default_hand_connections_style(),
    )
    return frame

def view_fingertip(frame, hand_landmarks):
    # Landmark 8 is the index fingertip (see the diagram above).
    tip = hand_landmarks.landmark[8]
    x, y = to_pixels(tip, frame.shape)
    cv2.circle(frame, (x, y), 10, (255, 0, 255), -1)
    cv2.putText(frame, f"({x}, {y})", (x + 15, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    return frame

def view_pinch(frame, hand_landmarks):
    thumb = to_pixels(hand_landmarks.landmark[4], frame.shape)   # thumb tip
    index = to_pixels(hand_landmarks.landmark[8], frame.shape)   # index tip

    distance = np.linalg.norm(np.array(thumb) - np.array(index))

    # Draw the line and the two ends
    cv2.line(frame, thumb, index, (0, 255, 255), 3)
    cv2.circle(frame, thumb, 10, (255, 0, 255), -1)
    cv2.circle(frame, index, 10, (255, 0, 255), -1)

    # A bar showing the distance. We assume 30..250 px is the useful range.
    pct = np.clip((distance - 30) / (250 - 30), 0, 1)
    cv2.rectangle(frame, (50, 400), (85, 150), (0, 255, 0), 2)
    bar_top = int(400 - pct * 250)
    cv2.rectangle(frame, (50, bar_top), (85, 400), (0, 255, 0), -1)
    cv2.putText(frame, f"{int(distance)}px", (40, 430),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return frame

def main():
    cap = open_camera()

    hands = mp_hands.Hands(
        static_image_mode=False,      # False = video mode, uses tracking
        max_num_hands=2,
        min_detection_confidence=0.7, # raise if it sees hands that aren't there
        min_tracking_confidence=0.5,
    )

    views = {ord("1"): ("skeleton", view_skeleton),
             ord("2"): ("fingertip", view_fingertip),
             ord("3"): ("pinch", view_pinch)}
    name, func = "skeleton", view_skeleton

    print("\nKeys:  1 skeleton | 2 fingertip | 3 pinch | q quit\n")

    while True:
        frame = read_frame(cap)
        if frame is None:
            break

        # MediaPipe wants RGB; OpenCV gives us BGR. This one line trips
        # up a LOT of people - without it, detection quietly gets worse.
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                frame = func(frame, hand_landmarks)
        else:
            cv2.putText(frame, "no hand detected", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(frame, name, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Hand tracking", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key in views:
            name, func = views[key]

    hands.close()
    cleanup(cap)


if __name__ == "__main__":
    main()