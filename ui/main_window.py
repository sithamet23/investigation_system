# ui/main_window.py (ฉบับอัปเดตสเต็ปที่ 11)
"""
Investigation Documents System - Main Window Component
Coordinates view transitions between HomeView, WarrantView, CaseView, and DocumentView.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QLabel,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from ui.components.topbar import TopBar
from ui.components.sidebar import Sidebar
from ui.views.home_view import HomeView
from ui.views.warrant_view import WarrantView
from ui.views.case_view import CaseView

# --- [แก้ไข/เพิ่มเติมจุดที่ 1: นำเข้าหน้าจอ DocumentView จริง] ---
from ui.views.document_view import DocumentView
import config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.setMinimumSize(1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.topbar = TopBar(self)
        self.main_layout.addWidget(self.topbar)

        self.body_layout = QHBoxLayout()
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(0)
        self.main_layout.addLayout(self.body_layout)

        self.sidebar = Sidebar(self)
        self.body_layout.addWidget(self.sidebar)

        self.content_stack = QStackedWidget()
        self.body_layout.addWidget(self.content_stack)

        # ลงทะเบียนหน้าจอตัวจริงทั้งหมดเข้าคลังระบบ
        self.home_view = HomeView(self)
        self.content_stack.addWidget(self.home_view)

        self.warrant_view = WarrantView(self)
        self.content_stack.addWidget(self.warrant_view)

        self.case_view = CaseView(self)
        self.content_stack.addWidget(self.case_view)

        # --- [แก้ไขจุดที่ 2: ติดตั้งอินสแตนซ์ DocumentView เข้าสู่แผงสลับหน้าจอ] ---
        self.document_view = DocumentView(self)
        self.content_stack.addWidget(self.document_view)

        self.sidebar.menu_changed.connect(self.handle_menu_navigation)
        self.sidebar.logout_requested.connect(self.handle_logout)

        self.content_stack.setCurrentWidget(self.home_view)

    # --- [แก้ไขจุดที่ 3: อัปเดตเงื่อนไขให้เปิดหน้า DocumentView เมื่อคลิกกลุ่มเมนูงานเอกสาร] ---
    def handle_menu_navigation(self, menu_name):
        """ประมวลผลการสลับมุมมองหน้าจอเมื่อผู้ใช้งานเลือกเมนู"""
        if menu_name == "Dashboard":
            self.content_stack.setCurrentWidget(self.home_view)
        elif menu_name == "ค้นหาข้อมูลหมายจับ":
            self.content_stack.setCurrentWidget(self.warrant_view)
        elif menu_name in [
            "ค้นหาสำนวนคดี",
            "เมาขับ",
            "เสพ",
            "การพนัน",
            "ผู้ประจำรถ",
            "ต่างด้าว",
        ]:
            self.content_stack.setCurrentWidget(self.case_view)
        elif menu_name in [
            "ค้นหาเอกสาร",
            "ขอทราบผลคดี",
            "แจ้งผลคดี",
            "แจ้งผลการส่งหมายเรียก",
            "แจ้งอายัด/ถอนอายัดผู้ต้องหา",
            "ขอถอนหมายจับ",
        ]:
            # ดักจับชื่อเมนูในกลุ่มงานเอกสารทั้งหมดให้ดีดมาเปิดที่หน้าจอควบคุมเอกสารร่วมกัน
            self.content_stack.setCurrentWidget(self.document_view)
        else:
            temp_view = QLabel(
                f"กำลังเปิดหน้างาน: [{menu_name}]\n(ขณะนี้อยู่ระหว่างพัฒนาเนื้อหาในสเต็ปถัดไป)"
            )
            temp_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
            temp_view.setStyleSheet(
                "font-size: 16px; color: #1A2B4C; background-color: #FFFFFF;"
            )
            self.content_stack.addWidget(temp_view)
            self.content_stack.setCurrentWidget(temp_view)

    def handle_logout(self):
        confirm = QMessageBox.question(
            self,
            "ยืนยันการออกจากระบบ",
            "คุณต้องการออกจากระบบงานตรวจสอบเอกสารใช่หรือไม่?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.close()
