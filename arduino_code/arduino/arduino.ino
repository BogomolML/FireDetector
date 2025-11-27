#include <Servo.h>

Servo servo_h;
Servo servo_v;
short lazer = 13;
float servo_angle_h, servo_angle_v;

void setup() {
  Serial.begin(9600);
  pinMode(lazer, OUTPUT);
  servo_v.attach(9);
  servo_h.attach(10);
  servo_v.write(90);
  servo_h.write(90);
}

void loop() {
  digitalWrite(lazer, HIGH);
  if (Serial.available()) {
    servo_angle_h = Serial.parseFloat(); //угол по горизонтали
    servo_angle_v = Serial.parseFloat(); //угол по вертикали
    while (Serial.available()) Serial.read();
    
    servo_h.write(servo_angle_h);
    servo_v.write(servo_angle_v);
  }
}