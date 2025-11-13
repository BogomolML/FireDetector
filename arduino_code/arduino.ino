#include <Servo.h>

Servo servo_h;
Servo servo_v;
float servo_angle_h, servo_angle_v;

void setup() {
  Serial.begin(9600);
  servo_h.attach(9);
  servo_v.attach(10);
  servo_h.write(90);
  servo_v.write(90);
}

void loop() {
  if (Serial.available()) {
    servo_angle_h = Serial.parseFloat(); //угол по горизонтали
    servo_angle_v = Serial.parseFloat(); //угол по вертикали
    while (Serial.available()) Serial.read();

    servo_h.write(servo_angle_h);
    servo_v.write(servo_angle_v);
  }
  delay(5000);
}