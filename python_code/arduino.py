import serial

from fire_detector import init_cap, main
from calc_angle import angles_to_servo_commands

ser = serial.Serial('COM3', 9600)
cap = init_cap()

while True:
    servo_h, servo_v = 0, 0
    cell = main(cap)
    print(cell)
    if cell == -1:
        break
    elif cell != 0 and cell.is_integer():
        servo_h, servo_v = angles_to_servo_commands(cell)
        ser.write(str(servo_h).encode('ascii'))
        ser.write(str(servo_v).encode('ascii'))
