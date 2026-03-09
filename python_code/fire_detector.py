from camera import Camera


def init_cap():
    cap = Camera()
    cap.init_camera()
    print("Нажмите 'q' чтобы выйти")
    return cap


def fire_detect(cap, yolo, display_thread):
    fire_center = 0

    while display_thread.running:
        frame = cap.capture_frame()
        if frame is not None:
            found, box = cap.detect_object(frame, yolo)

            if found:
                x1, y1, x2, y2 = box
                center = cap.get_center()
                print(center)
                if center is not None:
                    fire_center = (int(center[0]), int(center[1]))
                    display_thread.obj = ((x1, y1), (x2, y2))
                    display_thread.update_frame(frame)
                    return fire_center
            else:
                display_thread.obj = (-1, -1, -1, -1)
                display_thread.update_frame(frame)
    return -1
