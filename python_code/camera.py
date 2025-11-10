import cv2


class Camera:
    def __init__(self):
        self.camera = None
        self.fire = ()

    def init_camera(self):
        try:
            self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            print("Камера инициализирована")
        except Exception as e:
            print(f"Ошибка инициализации: {e}")

    def capture_frame(self):
        if self.camera:
            ret, frame = self.camera.read()
            if ret:
                return frame
        return None

    def detect_object(self, frame, cascade):
        if frame is None:
            return False, None

        self.fire = cascade.detectMultiScale(frame, 1.05, 4)
        if self.fire is not ():
            return True, self.fire[0]
        return False, None

    def get_center(self):
        try:
            x, y, w, h = self.fire[0]
            center = (x + w / 2, y + h / 2)
            return center
        except IndexError:
            print('Не определён огонь')
            return None

    def release_camera(self):
        if self.camera:
            self.camera.release()
