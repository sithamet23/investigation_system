from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
import config


class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 1. กำหนดโครงสร้างแบบแนวนอน และใส่สีพื้นหลังตามโทนที่กำหนดใน UI DESIGN
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        self.setStyleSheet(f"background-color: {config.PRIMARY_NAV_BG};")

        # 2. โซนฝั่งซ้าย: โลโก้จำลอง และ ชื่อระบบงาน
        # ในที่นี้จะใช้เครื่องหมาย ⚖️ เป็น Visual Anchor แทนโลโก้ส่วนราชการเบื้องต้น
        self.logo_label = QLabel("⚖️")
        self.logo_label.setStyleSheet("font-size: 20px; margin-right: 5px;")

        self.title_label = QLabel(config.APP_NAME)
        self.title_label.setStyleSheet(
            "color: #FFFFFF; font-size: 16px; font-weight: bold;"
        )

        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)

        # 3. ตัวคั่นกลาง (Spacer) เพื่อดันข้อมูลผู้ใช้งานไปชิดขวาสุดของหน้าจอ
        spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        layout.addItem(spacer)

        # 4. โซนฝั่งขวา: แสดงยศ-ชื่อผู้ปฏิบัติงาน และเวอร์ชันโปรแกรม
        user_info = f"ผู้ใช้งาน: {config.CURRENT_USER}  |  v{config.APP_VERSION}"
        self.user_label = QLabel(user_info)
        self.user_label.setStyleSheet("color: #E2EAF4; font-size: 13px;")
        self.user_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        layout.addWidget(self.user_label)
