from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import config


class StatCard(QWidget):
    def __init__(
        self, title, value="0", bg_color="#FFFFFF", text_color="#1A2B4C", parent=None
    ):
        super().__init__(parent)
        self.bg_color = bg_color
        self.text_color = text_color
        self.init_ui(title, value)

    def init_ui(self, title, value):
        # 1. จัดเลย์เอาต์แนวตั้งและกำหนดระยะขอบภายในตัวการ์ด
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # 2. ป้ายข้อความหัวข้อ (Title Label เช่น ยอดรวมหมายจับ)
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(
            f"color: {self.text_color}; font-size: 14px; font-weight: bold;"
        )
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # 3. ตัวเลขแสดงผลสถิติหลัก (Value Label)
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet(
            f"color: {self.text_color}; font-size: 28px; font-weight: bold;"
        )
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

        # 4. ติดตั้งสไตล์และสีพื้นหลังของการ์ดใบนี้
        self.update_card_style()

    def update_card_style(self):
        """กำหนดขอบมนและความลึกตื้นของการ์ดตาม UI Token"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.bg_color};
                border: 1px solid #D2DCFF;
                border-radius: 8px;
            }}
        """)

    def set_value(self, new_value):
        """ฟังก์ชันสำหรับ Slots ใช้เปลี่ยนตัวเลขบนการ์ดแบบไดนามิกเมื่อฐานข้อมูลอัปเดต"""
        self.value_label.setText(str(new_value))
