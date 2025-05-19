import cv2
from ultralytics import YOLO
import numpy as np

# Mở camera
img = cv2.VideoCapture(0)

# Tải mô hình YOLO
model = YOLO("best.pt")

# Ngưỡng chấp nhận
acceptance_threshold = 0.9

# Vùng phát hiện (x1, y1, x2, y2)
detection_zone = (100, 100, 200, 200)

# Biến đếm và danh sách ID vật thể đã được đếm
count = 0
detected_ids = set()

while True:
    ret, image = img.read()
    if not ret:
        break

    results = model(image)

    for result in results:
        boxes = result.boxes.xyxy
        scores = result.boxes.conf
        labels = result.boxes.cls

        for i, (box, score, class_id) in enumerate(zip(boxes, scores, labels)):
            x1, y1, x2, y2 = map(int, box)
            confidence = float(score)
            class_id = int(class_id)

            # Tên lớp
            class_name = result.names.get(class_id, "Unknown")
            label_text = f"{class_name}: {confidence:.2f}"

            if confidence >= acceptance_threshold:
                # Vẽ hộp vật thể
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 1)
                cv2.putText(image, label_text, (x1, y2 - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                # Tính trung tâm vật thể
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # Vẽ chấm tại trung tâm
                cv2.circle(image, (center_x, center_y), 1, (0, 255, 255), -1)

                # Kiểm tra nếu trung tâm nằm trong vùng phát hiện
                zone_x1, zone_y1, zone_x2, zone_y2 = detection_zone
                if zone_x1 < center_x < zone_x2 and zone_y1 < center_y < zone_y2:
                    # Tạo ID riêng cho mỗi bounding box (nếu không có ID, dùng toạ độ thay thế)
                    # object_id = f"{class_id}-{x1}-{y1}-{x2}-{y2}"
                    object_id = f"{class_id} - {x1}"
                    if object_id not in detected_ids:
                        count += 1
                        detected_ids.add(object_id)

    # Vẽ vùng phát hiện
    cv2.rectangle(image, (detection_zone[0], detection_zone[1]), (detection_zone[2], detection_zone[3]), (0, 255, 0), 2)
    cv2.putText(image, f"Count: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Hiển thị hình ảnh
    cv2.imshow("YOLOv8 Detection", image)
    if cv2.waitKey(1) == ord('q'):
        break

# Giải phóng tài nguyên
img.release()
cv2.destroyAllWindows()
