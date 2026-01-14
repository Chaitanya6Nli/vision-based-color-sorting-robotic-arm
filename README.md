# Vision-Based Color Sorting Robotic Arm 🤖🎨

This project focuses on building a **vision-based robotic arm** that can detect object colors and sort them automatically.  
Instead of relying on fixed positions or hardcoded logic, the robot observes its workspace through a camera, makes decisions in real time, and performs smooth pick-and-place operations.

The goal was to simulate a **real-world industrial sorting system** where vision, decision-making, and actuation work together.

---

## 🔍 Project Overview

The robotic arm uses a camera and computer vision to identify object colors (Green and Blue).  
Based on the detected color and user selection, the robot dynamically chooses the correct pick position and sorts the object into the appropriate bin.

---

## 📂 Code Structure

- `main_controller.py`  
  Handles camera input, color detection, keyboard control, decision-making, and serial communication with the robotic arm.

- `arduino_code.ino`  
  Controls servo motors and executes commands received from Python via serial communication.

---

## ⚙️ Key Features

- Color detection using **OpenCV**
- Dynamic selection of pick positions (no hardcoding)
- Smooth servo-controlled robotic arm motion
- Manual teaching of pick positions with saved reuse
- Automated color-based sorting logic
- Integration of **Python**, **Arduino**, and hardware control

---

## 🧠 Workflow

1. Manually teach pick positions for Target 1 and Target 2  
2. Camera continuously monitors the workspace  
3. User selects the desired color (Green / Blue)  
4. Robot detects the object color  
5. Robotic arm picks the object and sorts it into the correct bin  

---

## 🛠️ Technologies Used

- Python  
- OpenCV  
- Arduino  
- Servo Motors  
- Robotics & Automation Concepts  

---

## 👥 Team Members

- Kundan Bodkhe
- Chaitanya Belekar
- Arnab Nath
- Sanmitra Dhamane

---

## 📌 Future Improvements
  
- Improve object detection accuracy
- voice controlled based inputs
- Implement full automation without user color selection  
- Agentic AI based decision-making  

---

## 📷 Demo

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/f9804cf4-fec4-41ad-ae7c-1000530aaa33" />
<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/9e99acb4-d5b3-4ae6-8270-c3f219ec2478" />
<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/5b448636-2558-4f27-913d-232ab991dd0d" />

https://github.com/user-attachments/assets/58ca5c0b-6671-4cd8-b82f-40362ce6ed13


