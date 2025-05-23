import cv2
from ultralytics import YOLO
import numpy as np
import time
import os
import threading

img = cv2.VideoCapture(0)

# Tải mô hình đã huấn luyện (best.pt)
model = YOLO("best.pt")

# Ngưỡng chấp nhận (confidence threshold)
acceptance_threshold = 0.6

last_time_detect = 0
image_detect_display = None
detect_count = 0

# Đọc ảnh
#image = cv2.imread(r"D:\12.python\HT\HTXLA\picture39.jpg")
def detect(image_detect, detect_id):
    results = model(image_detect)
    name_file = "D:/Xulyanhmau/picture_bai2/" + str(detect_id) + ".jpg"
    global image_detect_display # dinh nghia no la bien toan cuc
    global detect_count
    # Duyệt qua kết quả
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # Tọa độ hộp: x1, y1, x2, y2
        scores = result.boxes.conf.cpu().numpy()  # Độ tin cậy
        labels = result.boxes.cls.cpu().numpy()   # Nhãn (ID lớp)

        for box, score, class_id in zip(boxes, scores, labels):
            x1, y1, x2, y2 = map(int, box)
            confidence = float(score)
            class_id = int(class_id)

            # Tên lớp từ model
            class_name = result.names.get(class_id, "Unknown")
            label_text = f"{class_name}: {confidence:.2f}"

            # Nếu đủ độ tin cậy thì vẽ
            if confidence >= acceptance_threshold:
                cv2.rectangle(image_detect, (x1, y1), (x2, y2), (255, 0, 0), 1)
                cv2.putText(image_detect, label_text, (x1, y2 - 1),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                #cv2.imwrite(name_file,image_detect)
                image_detect_display = image_detect
                detect_count += 1
                #img_detect = 

        

while True:
    ret,image = img.read()

    if not ret or image is None:
        continue
    #xacdinhkhoi(image)
    cv2.putText(image, f"Detect count:  {detect_count}", (1,18),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
    cv2.imshow("Stream", image)

    current_time = time.time()
    # Chạy mô hình
    
    if current_time - last_time_detect >= 0.5:
        last_time_detect = current_time

    #tao ban sao de detect
        image_detect = image.copy()
        detect_id = int(current_time)

        #Tao va chay luong detect
        t = threading.Thread(target= detect,args=(image_detect,detect_id))
        t.start()
    
    if image_detect_display is not None:
        cv2.imshow("Detection", image_detect_display)
    
    #if cv2.waitKey(1) == ord('q'):
    if cv2.waitKey(1) == 27:
        break

img.release()
cv2.destroyAllWindows() 
