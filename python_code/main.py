from time import time, sleep

import cv2
import serial
from serial import SerialException

from UI import DisplayThread
from calc_angle import angles_to_servo_commands
from fire_detector import init_cap, fire_detect

PORT = 'COM3'
SEND_INTERVAL = 1

try:
    ser = serial.Serial(PORT, 9600)
except SerialException as e:
    print(e)
    exit(-1)

cap = init_cap()
fire_cascade = cv2.CascadeClassifier('fire_detection.xml')

display_thread = DisplayThread()
display_thread.start()

servo_h, servo_v = 90, 90
last_send_time = 0
try:
    while True:
        cell = fire_detect(cap, fire_cascade, display_thread)
        if cell == -1:
            break
        if cell != 0 and time() - last_send_time > SEND_INTERVAL:
            print(cell)
            servo_h, servo_v = angles_to_servo_commands(cell)
            message = f"{servo_h}\n{servo_v}\n"
            ser.write(message.encode('ascii'))
            last_send_time = time()
        sleep(0.01)
except SerialException as e:
    print(e)
finally:
    display_thread.stop()
    display_thread.join()
    cap.release_camera()
    cv2.destroyAllWindows()
    print("Программа завершена")