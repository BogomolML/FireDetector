from camera import Camera


def init_cap():
    cap = Camera()
    cap.init_camera()
    print("Нажмите 'q' чтобы выйти")
    return cap


def fire_detect(cap, fire_cascade, display_thread):
    fire_center = 0

    while display_thread.running:
        frame = cap.capture_frame()
        if frame is not None:
            found, box = cap.detect_object(frame, fire_cascade)

            if found:
                x, y, w, h = box
                center = cap.get_center()
                if center is not None:
                    # Возвращаем координаты центра огня (x, y)
                    fire_center = (int(center[0]), int(center[1]))
                    display_thread.obj = ((x, y), (x + w, y + h))
                    display_thread.update_frame(frame)
                    return fire_center
            else:
                display_thread.obj = ()
                display_thread.update_frame(frame)
    return -1
