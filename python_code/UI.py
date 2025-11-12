import threading
from queue import Queue

import cv2

from grid import get_grid_size


class DisplayThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.frame_queue = Queue(maxsize=1)
        self._running = True
        self.current_frame = None
        self._obj = ()

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, value):
        self._obj = value

    def update_frame(self, frame):
        if not self.frame_queue.empty():
            try:
                self.frame_queue.get_nowait()
            except:
                pass
        self.frame_queue.put(frame.copy())

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if not self.frame_queue.empty():
                self.current_frame = self.frame_queue.get()

            if self.current_frame is not None:
                draw_frame(self.current_frame, self.obj)
                cv2.imshow('Camera View', self.current_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
                break

        cv2.destroyAllWindows()


def draw_frame(frame, obj: tuple):
    h, w = frame.shape[:2]
    r, c = get_grid_size()
    color = (0, 0, 255)
    if len(obj) > 0:
        cv2.rectangle(frame, obj[0], obj[1], color, 2)
    for x in range(0, w - 1, w // r):
        cv2.line(frame, (x, 0), (x, h), color[::-1], 1, 1)
    for y in range(0, h - 1, h // c):
        cv2.line(frame, (0, y), (w, y), color[::-1], 1, 1)
