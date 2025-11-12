from camera import Camera
from grid import check_point


def init_cap():
    cap = Camera()
    cap.init_camera()
    print("Нажмите 'q' чтобы выйти")
    return cap

def fire_detect(cap, fire_cascade, display_thread):
    cell = 0

    while display_thread.running:
        frame = cap.capture_frame()
        if frame is not None:
            found, box = cap.detect_object(frame, fire_cascade)

            if found:
                x, y, w, h = box
                center = cap.get_center()
                cell = check_point(center, *frame.shape[:2])
                display_thread.obj = ((x, y), (x + w, y + h))
                display_thread.update_frame(frame)
                return cell
            else:
                display_thread.obj = ()
                display_thread.update_frame(frame)
    return -1
