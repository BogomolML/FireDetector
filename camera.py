import cv2

class Camera:
    def __init__(self):
        self.camera = None

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

    @staticmethod
    def detect_object(frame, cascade):
        if frame is None:
            return False, None

        fire = cascade.detectMultiScale(frame, 1.1, 5)
        if fire is not ():
            return True, fire[0]
        return False, None

    def release_camera(self):
        if self.camera:
            self.camera.release()