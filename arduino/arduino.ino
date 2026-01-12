#include <Servo.h>

Servo servo_h;
Servo servo_v;
float servo_angle_h, servo_angle_v;
short lazer = 13;

float center_h = 3.0f;
float center_v = 14.0f;

void setup() {
  Serial.begin(9600);
  servo_h.attach(9);
  servo_v.attach(10);

  servo_h.write(90 + center_h);
  servo_v.write(90 + center_v);

  pinMode(lazer, OUTPUT);
  digitalWrite(lazer, HIGH);
}

void loop() {
  if (Serial.available() >= 1) {
    String input_h = Serial.readStringUntil('\n');
    String input_v = Serial.readStringUntil('\n');
    
    if (input_h.length() > 0 && input_v.length() > 0) {
      servo_angle_h = input_h.toFloat() + center_h;
      servo_angle_v = input_v.toFloat() + center_v;
      
      servo_angle_h = constrain(servo_angle_h, 0, 180);
      servo_angle_v = constrain(servo_angle_v, 0, 180);
      
      servo_h.write((int)servo_angle_h);
      servo_v.write((int)servo_angle_v);
    }
  }
}