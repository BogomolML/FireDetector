from time import time, sleep

import cv2
import serial
from serial import SerialException

from UI import DisplayThread
from calc_angle import angles_to_servo_commands
from fire_detector import init_cap, fire_detect

SEND_INTERVAL = 1
PORT = 'COM8'

try:
    ser = serial.Serial(PORT, 9600)
except SerialException as e:
    print(e)
    exit(-1)

cap = init_cap()
fire_cascade = cv2.CascadeClassifier('fire_detection.xml')

display_thread = DisplayThread()
display_thread.start()

servo_h, servo_v = 0, 0
last_send_time = 0

center_h = -10
center_v = 0


try:
    while True:
        fire_center = fire_detect(cap, fire_cascade, display_thread)
        if fire_center == -1:
            break
        if fire_center != 0 and time() - last_send_time > SEND_INTERVAL:
            print(f"Огонь обнаружен в {fire_center}")

            frame = cap.capture_frame()
            if frame is not None:
                frame_size = frame.shape[:2]
                frame_size_reversed = (frame_size[1], frame_size[0])

                servo_h, servo_v = angles_to_servo_commands(fire_center, frame_size_reversed)
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
