from time import time, sleep

import cv2
import serial
from serial import SerialException
from ultralytics import YOLO

from UI import DisplayThread
from calc_angle import angles_to_servo_commands
from fire_detector import init_cap, fire_detect

SEND_INTERVAL = 3
PORT = 'COM8'

try:
    ser = serial.Serial(PORT, 9600)
except SerialException as e:
     print(e)
     exit(-1)

cap = init_cap()
old_fire_center = 0

yolo_1 = YOLO('models/yolov8_1.pt')
yolo_2 = YOLO('models/yolov8_2.pt')
yolo_3 = YOLO('models/yolo26n.pt')
yolo_4 = YOLO('models/yolo26s.pt')
yolos = (yolo_1, yolo_2, yolo_3, yolo_4)

display_thread = DisplayThread()
display_thread.start()

servo_h, servo_v = 0, 0
last_send_time = 0


try:
    while True:
        fire_center = fire_detect(cap, yolos, display_thread)
        if fire_center == -1:
            break
        if fire_center != 0 and time() - last_send_time > SEND_INTERVAL:
            if old_fire_center != 0:
                fire_center = old_fire_center
            print(f"Огонь обнаружен в {fire_center}")

            frame = cap.capture_frame()
            if frame is not None:
                frame_size = frame.shape[:2]
                frame_size_reversed = (frame_size[1], frame_size[0])

                servo_h, servo_v = angles_to_servo_commands(fire_center, frame_size_reversed)
                message = f"{servo_h}\n{servo_v}\n"
                ser.write(message.encode('ascii'))
                last_send_time = time()
            old_fire_center = 0
        else:
            old_fire_center = fire_center
        sleep(0.01)
except SerialException as e:
    print(e)
finally:
    display_thread.stop()
    display_thread.join()
    cap.release_camera()
    cv2.destroyAllWindows()
    print("Программа завершена")
