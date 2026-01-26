import threading
from queue import Queue

import cv2


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
    color = (0, 0, 255)
    x, y = frame.shape[:2]
    x, y = x // 2, y // 2
    cv2.circle(frame, (y, x), 3, color, -1)
    if len(obj) > 0:
        cv2.rectangle(frame, obj[0], obj[1], color, 2)
