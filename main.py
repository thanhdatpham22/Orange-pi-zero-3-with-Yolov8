#file chạy chính
import threading
import cv2
import time
from predict import detect_person
from rfid import read_rfid
from request_server import push_server

# Biến điều khiển luồng
stop_event = threading.Event()

def request_time():
    start_time=time.time()
    endtime=time.time()
    print(f"time: {start_time-endtime}")
    time.sleep(30)

if __name__ == "__main__":
    # Tạo và khởi chạy luồng
    thread_1 = threading.Thread(target=detect_person)
    thread_4 = threading.Thread()
    #thread_2 = threading.Thread(target=read_rfid)
    #thread_3 = threading.Thread(target=push_server)

    thread_1.start()

    #thread_2.start()

    #thread_3.start()

    # Đợi một khoảng thời gian rồi dừng tất cả luồng
    time.sleep(50)
    #stop_event.set()

    thread_1.join()
    #thread_2.join()
    #thread_3.join()

