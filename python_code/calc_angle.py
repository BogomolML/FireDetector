from grid import COLS, ROWS

HFOV, VFOV = 60, 34.3

def cell_to_angles(cell: int) -> tuple:
    row = (cell - 1) // COLS
    col = (cell - 1) % COLS

    norm_x = (col - (COLS - 1) / 2) / ((COLS - 1) / 2)
    norm_y = (row - (ROWS - 1) / 2) / ((ROWS - 1) / 2)

    angle_h = norm_x * (HFOV / 2)
    angle_v = norm_y * (VFOV / 2)
    return angle_h, angle_v

def angles_to_servo_commands(cell: int) -> tuple:
    angle_h, angle_v = cell_to_angles(cell)
    servo_h = round(90 + angle_h, 2)
    servo_v = round(90 + angle_v, 2)
    return servo_h, servo_v
