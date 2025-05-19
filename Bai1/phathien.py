import cv2
from ultralytics import YOLO
import numpy as np

img = cv2.VideoCapture(0)

# Tải mô hình đã huấn luyện (best.pt)
model = YOLO("best.pt")

# Ngưỡng chấp nhận (confidence threshold)
acceptance_threshold = 0.6

# Đọc ảnh
while True:
    _,image = img.read()

    # Chạy mô hình
    results = model(image)

    # Duyệt qua kết quả
    for result in results:
        boxes = result.boxes.xyxy  # Tọa độ hộp: x1, y1, x2, y2
        scores = result.boxes.conf  # Độ tin cậy
        labels = result.boxes.cls   # Nhãn (ID lớp)

        for box, score, class_id in zip(boxes, scores, labels):
            x1, y1, x2, y2 = map(int, box)
            confidence = float(score)
            class_id = int(class_id)

            # Tên lớp từ model
            class_name = result.names.get(class_id, "Unknown")
            label_text = f"{class_name}: {confidence:.2f}"

            # Nếu đủ độ tin cậy thì vẽ
            if confidence >= acceptance_threshold:
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.putText(image, label_text, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

    # Hiển thị ảnh
    cv2.imshow("YOLOv8 Detection", image)
    if cv2.waitKey(1) == ord('q'):
        break
img.release()
cv2.destroyAllWindows()
