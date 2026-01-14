
#include <Servo.h>

// Servos
Servo base, shoulder, elbow, pitch, roll, gripper;

// Pins
int BASE_PIN = 3;
int SHOULDER_PIN = 5;
int ELBOW_PIN = 6;
int PITCH_PIN = 9;
int ROLL_PIN = 10;
int GRIPPER_PIN = 11;

// Calibration
int BASE_HOME = 130;
int SHOULDER_ZERO = 42;
int ELBOW_ZERO = 75;
int PITCH_ZERO = 0;
int ROLL_ZERO = 80;

void setup() {
  Serial.begin(9600);

  base.attach(BASE_PIN);
  shoulder.attach(SHOULDER_PIN);
  elbow.attach(ELBOW_PIN);
  pitch.attach(PITCH_PIN);
  roll.attach(ROLL_PIN);
  gripper.attach(GRIPPER_PIN);

  // Home position
  base.write(BASE_HOME);
  shoulder.write(SHOULDER_ZERO);
  elbow.write(ELBOW_ZERO);
  pitch.write(PITCH_ZERO);
  roll.write(ROLL_ZERO);
  gripper.write(150);

  Serial.println("READY");
}

void loop() {
  if (Serial.available()) {
    int b = Serial.parseInt();
    int s = Serial.parseInt();
    int e = Serial.parseInt();
    int p = Serial.parseInt();
    int r = Serial.parseInt();
    int g = Serial.parseInt();

    if (Serial.read() == '\n') {
      base.write(b);
      shoulder.write(SHOULDER_ZERO + s);
      elbow.write(ELBOW_ZERO + e);
      pitch.write(PITCH_ZERO + p);
      roll.write(ROLL_ZERO + r);
      gripper.write(g);
    }
  }
}
