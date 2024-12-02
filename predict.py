import cv2
import time
from ultralytics import YOLO
import threading

model = YOLO('yolov8n.pt')
stop_event = threading.Event()
# img_path = 'C:/Users/MyPC/Desktop/Machine_learning/YOLO/YOLOv8/DATA/zidane.jpg'
# img_path = 'C:/Users/MyPC/Desktop/Machine_learning/DATASET/video_test/ngoaitroi3.mp4'

#path_in = "/home/orangepi/YOLOv8/test3.jpg"
#path_out ="/home/orangepi/YOLOv8"
count = 0
# fps = 30
# # # Set kich thuoc khung hinh moi
# ret = cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
# ret = cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
def detect_person():
    cap = cv2.VideoCapture(0)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # print("Kich thuc khung hinh:%dx%d, FPS = %d" %(w,h,fps) )
    #save_video = cv2.VideoWriter(path_out, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h)) # khoi tao doi tuong luu video
    while not stop_event.is_set():
    #while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, classes=0)

        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        #cv2.imwrite("result.png", annotated_frame)  ## save image
        # save_video.write(annotated_frame) # save video

    # time.sleep(5)
        if results[0]:
            #count = results[0].__len__()
            #print(count)
            print(results[0].names[int(results[0].boxes.cls[0])], results[0].__len__())  # results[0] la ket qua cua batch=1
        else:
            print(0)
    # print(results[0].boxes.data)
    # print(results[0].boxes.cpu().numpy())
    # det = model.batch[1]
    # print(det)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_person()