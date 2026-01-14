import serial
import time
import keyboard
import cv2
import numpy as np
import json
import os

# SERIAL
ser = serial.Serial('COM7', 9600)
time.sleep(2)

# SORT MOTIONS
BASE_GREEN = 100        # GREEN
BASE_BLUE = 90          # BLUE
SHOULDER_GREEN_DROP = -28
ELBOW_EXT = -30
ELBOW_DROP = 16

# HOME 
HOME = {
    "base": 130,
    "shoulder": 0,
    "elbow": 0,
    "pitch": 0,
    "roll": 0,
    "gripper": 150
}

state = HOME.copy()

# TARGET STORAGE
SAVE_FILE = "targets01.json"

target_1 = []
target_2 = []
current_target = 1

# SPEED 
STEP = 1
DELAY = 0.03

# CAMERA MEMORY
last_detected_color = None
last_detected_target = None

# LOAD SAVED TARGETS
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
        target_1 = data.get("target_1", [])
        target_2 = data.get("target_2", [])
    print(" Target sequences loaded")

# SAVE TARGETS 
def save_targets():
    with open(SAVE_FILE, "w") as f:
        json.dump({
            "target_1": target_1,
            "target_2": target_2
        }, f, indent=2)
    print(" Targets saved")

# SEND 
def send():
    cmd = f"{state['base']},{state['shoulder']},{state['elbow']}," \
          f"{state['pitch']},{state['roll']},{state['gripper']}\n"
    ser.write(cmd.encode())

# SMOOTH MOVE
def move_smooth(target, steps=30):
    global state
    start = state.copy()
    for i in range(1, steps + 1):
        for j in state:
            state[j] = int(start[j] + (target[j] - start[j]) * i / steps)
        send()
        time.sleep(DELAY)

# CAMERA
cap = cv2.VideoCapture(0)
time.sleep(2)

if not cap.isOpened():
    print("Camera failed")
    exit()

# COLOR + TARGET DETECTION 
def detect_color_and_target(frame, color):
    blur = cv2.GaussianBlur(frame, (7,7), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    if color == "green":
        lower = np.array([35, 80, 80])
        upper = np.array([85, 255, 255])
    else:
        lower = np.array([100, 120, 80])
        upper = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    c = max(contours, key=cv2.contourArea)
    if cv2.contourArea(c) < 1200:
        return None

    x, y, w, h = cv2.boundingRect(c)
    cx = x + w // 2
    return 1 if cx < frame.shape[1] // 2 else 2

print(" Robot ready")
print("1/2 → Select Target | P → Save Pose")
print("5 → Auto pick | H → Home | X → Exit")

# MAIN LOOP 
while True:

    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    cv2.line(frame, (w//2,0), (w//2,h), (255,255,255), 2)
    cv2.imshow("Camera Feed", frame)
    cv2.waitKey(1)

    # CONTINUOUS DETECTION
    for c in ["green", "blue"]:
        t = detect_color_and_target(frame, c)
        if t:
            last_detected_color = c
            last_detected_target = t

    # MANUAL JOG 
    if keyboard.is_pressed('w'): state['shoulder'] += STEP
    if keyboard.is_pressed('s'): state['shoulder'] -= STEP
    if keyboard.is_pressed('e'): state['elbow'] += STEP
    if keyboard.is_pressed('d'): state['elbow'] -= STEP
    if keyboard.is_pressed('a'): state['base'] += STEP
    if keyboard.is_pressed('f'): state['base'] -= STEP
    if keyboard.is_pressed('r'): state['pitch'] += STEP
    if keyboard.is_pressed('t'): state['pitch'] -= STEP
    if keyboard.is_pressed('q'): state['roll'] += STEP
    if keyboard.is_pressed('z'): state['roll'] -= STEP
    if keyboard.is_pressed('o'): state['gripper'] += STEP
    if keyboard.is_pressed('c'): state['gripper'] -= STEP

    # TARGET SELECT
    if keyboard.is_pressed('1'):
        current_target = 1
        print(" Target 1")
        time.sleep(0.4)

    if keyboard.is_pressed('2'):
        current_target = 2
        print(" Target 2")
        time.sleep(0.4)

    # SAVE POSE 
    if keyboard.is_pressed('p'):
        if current_target == 1:
            target_1.append(state.copy())
        else:
            target_2.append(state.copy())
        save_targets()
        time.sleep(0.4)

    # AUTO PICK
    if keyboard.is_pressed('5'):
        print("Press G (GREEN) or B (BLUE)")
        desired = None
        while desired is None:
            if keyboard.is_pressed('g'): desired = "green"
            if keyboard.is_pressed('b'): desired = "blue"

        if last_detected_color != desired:
            print(" Color not visible")
            continue

        seq = target_1 if last_detected_target == 1 else target_2
        print(f"Picking {desired.upper()}")

        for pose in seq:
            move_smooth(pose)

        state["base"] = BASE_GREEN if desired == "green" else BASE_BLUE
        move_smooth(state)

        if desired == "green":
            g = state.copy()
            g["shoulder"] += SHOULDER_GREEN_DROP
            g["elbow"] += ELBOW_EXT
            move_smooth(g)
            state = g.copy()

        d = state.copy()
        d["elbow"] += ELBOW_DROP
        move_smooth(d)
        state = d.copy()

        o = state.copy()
        o["gripper"] = 150
        move_smooth(o)
        state = o.copy()

        move_smooth(HOME)
        state = HOME.copy()
        send()

        print(" Done")

    if keyboard.is_pressed('h'):
        move_smooth(HOME)
        state = HOME.copy()

    if keyboard.is_pressed('x'):
        break

    send()
    time.sleep(DELAY)

cap.release()
cv2.destroyAllWindows()
