import threading

import cv2

stop_event = threading.Event()
def detect_person(stop_event):
    cap = cv2.VideoCapture(1)
    while not stop_event.is_set():
        ret, frame = cap.read()
        if ret:
            # Thực hiện nhận diện người tại đây
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    detect_person(stop_event)