import cv2
from camera import Camera

from grid import check_point, get_grid_size

def init_cap():
    cap = Camera()
    cap.init_camera()
    print("Нажмите 'q' чтобы выйти")
    return cap

def main(cap, fire_cascade):
    cell = 0

    while True:
        frame = cap.capture_frame()
        if frame is not None:
            found, box = cap.detect_object(frame, fire_cascade)

            if found:
                x, y, w, h = box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow('Camera View', frame)
                center = cap.get_center()
                cell = check_point(center, *frame.shape[:2])
                return cell

            h, w = frame.shape[:2]
            r, c = get_grid_size()
            color = (0, 0, 255)
            for x in range(0, w - 1, w // r):
                cv2.line(frame, (x, 0), (x, h), color[::-1], 1, 1)
            for y in range(0, h - 1, h // c):
                cv2.line(frame, (0, y), (w, y), color[::-1], 1, 1)
            cv2.imshow('Camera View', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
