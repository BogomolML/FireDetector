import cv2
import numpy as np


SCALE_FACTOR = 1.05
MIN_NEIGHBORS = 1


class Camera:
    def __init__(self):
        self.camera = None
        self.fire = (-1, -1, -1, -1)

    def init_camera(self):
        try:
            self.camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
            print("Камера инициализирована")
        except Exception as e:
            print(f"Ошибка инициализации: {e}")

    def capture_frame(self):
        if self.camera:
            ret, frame = self.camera.read()
            if ret:
                return frame
        return None

    def detect_object(self, frame, yolo):
        if frame is None:
            return False, None

        results = yolo(frame)[0]
        classes_names = results.names
        classes = results.boxes.cls.cpu().numpy()
        boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)

        grouped_obj = {}
        for class_id, box in zip(classes, boxes):
            class_name = classes_names[int(class_id)]
            if class_name not in grouped_obj:
                grouped_obj[class_name] = []
            grouped_obj[class_name].append(box)

        if 'Fire' not in grouped_obj.keys():
            return False, None

        area = (self.fire[2] - self.fire[0]) * (self.fire[3] * self.fire[1])
        for x1, y1, x2, y2 in grouped_obj['Fire']:
            if (x2 - x1) * (y2 - y1) > area:
                self.fire = (x1, y1, x2, y2)
        return True, self.fire

    def get_center(self):
        try:
            x1, y1, x2, y2 = self.fire
            center = (x1 + (x2 - x1) / 2, y2)
            return center
        except IndexError:
            print('Не определён огонь')
            return None

    def release_camera(self):
        if self.camera:
            self.camera.release()
