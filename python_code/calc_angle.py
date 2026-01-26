HFOV, VFOV = 48, 34.3


def cell_to_angles(coord: tuple, frame_size: tuple) -> tuple:
    x, y = coord
    cols, rows = frame_size

    norm_x = (x - (cols - 1) / 2) / ((cols - 1) / 2)
    norm_y = (y - (rows - 1) / 2) / ((rows - 1) / 2)

    radial_distance = (norm_x ** 2 + norm_y ** 2) ** 0.5

    if norm_y < 0:  # Верх кадра
        vertical_factor = 1.5  # Усиление для верха
    else:
        vertical_factor = 1.0

    k_correction = 1.0 + 0.2 * radial_distance * vertical_factor

    angle_h = norm_x * (HFOV / 2) * k_correction
    angle_v = norm_y * (VFOV / 2) * k_correction
    print(angle_h, angle_v)
    return angle_h, angle_v


def angles_to_servo_commands(coord: tuple, frame_size: tuple) -> tuple:
    angle_h, angle_v = cell_to_angles(coord, frame_size)
    servo_h = round(90 + angle_h, 2)
    servo_v = round(90 - angle_v, 2)
    return servo_h, servo_v
