# code_train

import torch
print(torch.cuda.is_available())
from ultralytics import YOLO
import wandb

# Đăng nhập vào Weights & Biases (W&B) để theo dõi quá trình huấn luyện (tuỳ chọn)
#wandb.login(key="38f8ad7ec777cb01a116465827f9f72f7207f22")

# Tải mô hình YOLOv8n (lightweight)
model = YOLO("yolov8s.pt")
# Nếu muốn tiếp tục huấn luyện từ lần huấn luyện trước:
#model = YOLO("last.pt")

# Bắt đầu huấn luyện
model.train(
    data= "data.yaml",
    epochs=100,
    imgsz=640,
    batch=16,
    project="my-yolo-project",
    name="yolov8-custom"
)

