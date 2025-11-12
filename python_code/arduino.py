import serial
from serial import SerialException
import cv2

from fire_detector import init_cap, main
from calc_angle import angles_to_servo_commands

try:
    ser = serial.Serial('COM3', 9600)
except SerialException as e:
    print(e)
    exit(-1)
cap = init_cap()
fire_cascade = cv2.CascadeClassifier('fire_detection.xml')


try:
    while True:
        servo_h, servo_v = 0, 0
        cell = main(cap, fire_cascade)
        print(cell)
        if cell == -1:
            break
        elif cell != 0:
            servo_h, servo_v = angles_to_servo_commands(cell)
            message = f"{servo_h}\n{servo_v}\n"
            ser.write(message.encode('ascii'))
except SerialException as e:
    print(e)
finally:
    cap.release_camera()
    cv2.destroyAllWindows()
    print("Программа завершена")