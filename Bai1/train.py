# code_train

import torch
from ultralytics import YOLO
import wandb

# Đăng nhập vào Weights & Biases (W&B) để theo dõi quá trình huấn luyện (tuỳ chọn)
#wandb.login(key="38f8ad7ec777cb01a116465827f9f72f7207f22")

# Tải mô hình YOLOv8n (lightweight)
#model = YOLO("yolov8n.pt")
# Nếu muốn tiếp tục huấn luyện từ lần huấn luyện trước:
model = YOLO(r"D:\5.HT\HTVAXLA\dataset\last.pt")

# Bắt đầu huấn luyện
model.train(
    data= "D:/5.HT/HTVAXLA/dataset/data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    project="my-yolo-project",
    name="yolov8n-custom"
)

