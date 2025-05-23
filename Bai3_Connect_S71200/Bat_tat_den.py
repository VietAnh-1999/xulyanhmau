import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
import snap7
#branch battatden Ui

class PLCControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Điều khiển và đọc trạng thái đèn PLC")
        self.setFixedSize(300, 200)

        # Kết nối PLC
        self.plc = snap7.client.Client()
        try:
            self.plc.connect("192.168.0.154", 0, 1)
        except Exception as e:
            print("Không kết nối được PLC:", e)

        # Các nút
        self.button_on = QPushButton("BẬT ĐÈN")
        self.button_off = QPushButton("TẮT ĐÈN")
        self.status_label = QLabel("Trạng thái: ?")
        self.status_label.setStyleSheet("font-size: 18px;")

        self.button_on.clicked.connect(self.turn_on)
        self.button_off.clicked.connect(self.turn_off)

        layout = QVBoxLayout()
        layout.addWidget(self.button_on)
        layout.addWidget(self.button_off)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        # Timer đọc trạng thái mỗi 1 giây
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)  # 1000 ms = 1 giây

    def write_bool(self, db_num, byte_index, bit_index, value):
        try:
            data = self.plc.db_read(db_num, byte_index, 1)
            snap7.util.set_bool(data, 0, bit_index, value)
            self.plc.db_write(db_num, byte_index, data)
        except Exception as e:
            print("Lỗi ghi dữ liệu:", e)

    def read_bool(self, db_num, byte_index, bit_index):
        try:
            data = self.plc.db_read(db_num, byte_index, 1)
            return snap7.util.get_bool(data, 0, bit_index)
        except Exception as e:
            print("Lỗi đọc dữ liệu:", e)
            return None

    def turn_on(self):
        self.write_bool(1, 0, 0, True)

    def turn_off(self):
        self.write_bool(1, 0, 0, False)

    def update_status(self):
        state = self.read_bool(1, 0, 0)  # DB1.DBB0.0
        if state is not None:
            self.status_label.setText(f"Trạng thái: {'🟢 BẬT' if state else '⚪ TẮT'}")
        else:
            self.status_label.setText("Trạng thái: lỗi đọc")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PLCControlApp()
    window.show()
    sys.exit(app.exec_())
