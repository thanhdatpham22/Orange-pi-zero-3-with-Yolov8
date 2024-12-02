import threading
import cv2
import time
from vd2 import detect_person
# Biến điều khiển luồng
stop_event = threading.Event()




def read_rfid():
    cnt = 0
    while not stop_event.is_set():
        # Thực hiện đọc RFID tại đây
        time.sleep(1)  # Giả sử việc đọc RFID mất 1 giây
        print("RFID read {}".format(cnt))
        cnt += 1


def manage_camera():
    while not stop_event.is_set():
        # Tạo một biến điều khiển mới cho mỗi lần khởi động luồng camera
        camera_stop_event = threading.Event()
        camera_thread = threading.Thread(target=detect_person, args=(camera_stop_event,))
        camera_thread.start()

        # Chạy camera trong 10 giây
        time.sleep(30)
        camera_stop_event.set()  # Dừng luồng camera
        camera_thread.join()  # Đợi cho đến khi luồng camera kết thúc

        # Đợi 30 giây trước khi bật lại camera
        time.sleep(30)


if __name__ == "__main__":
    # Tạo và khởi chạy luồng đọc RFID
    rfid_thread = threading.Thread(target=read_rfid)
    rfid_thread.start()

    # Quản lý việc bật và tắt camera
    manage_camera_thread = threading.Thread(target=manage_camera)
    manage_camera_thread.start()

    # Đợi một khoảng thời gian rồi dừng tất cả luồng
    # Ví dụ: chạy trong 120 giây rồi dừng
    #time.sleep(120)
    #stop_event.set()

    rfid_thread.join()
    manage_camera_thread.join()