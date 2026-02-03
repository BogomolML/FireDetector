#include <Servo.h>


Servo servo_h;
Servo servo_v;

float servo_angle_h, servo_angle_v;
int8_t lazer = 13;
int8_t RELAY_PIN = 2;

int8_t pump_time = 5;

int32_t now_time = 0;
int32_t turn_on_time = 0;

int8_t center_h = -11;
int8_t center_v = -10;

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);

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
      servo_angle_h = input_h.toInt() + center_h;
      servo_angle_v = input_v.toInt() + center_v;
      
      servo_angle_h = constrain(servo_angle_h, 0, 180);
      servo_angle_v = constrain(servo_angle_v, 0, 180);
      
      servo_h.write(servo_angle_h);
      servo_v.write(servo_angle_v);

      digitalWrite(RELAY_PIN, LOW);
      turn_on_time = millis();

      while (millis() - turn_on_time <= 5000) {}
      digitalWrite(RELAY_PIN, HIGH);
    }
  }
}