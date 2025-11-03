import cv2
from camera import Camera


cap = Camera()
cap.init_camera()

fire_cascade = cv2.CascadeClassifier('fire_detection.xml')

print("Нажмите 'q' чтобы выйти")

while True:
    frame = cap.capture_frame()
    if frame is not None:
        found, box = cap.detect_object(frame, fire_cascade)

        if found:
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Camera View', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release_camera()
cv2.destroyAllWindows()
print("Программа завершена")
