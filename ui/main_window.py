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

# --- [แก้ไข/เพิ่มเติมจุดที่ 1: นำเข้าคอมโพเนนต์ Sidebar จริง] ---
from ui.components.sidebar import Sidebar
import config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.setMinimumSize(1200, 800)

        # 1. แผงควบคุมเลย์เอาต์แนวตั้งหลัก
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 2. เพิ่มส่วนหัวของแอป (TopBar)
        self.topbar = TopBar(self)
        self.main_layout.addWidget(self.topbar)

        # 3. โครงสร้างแบ่งพื้นที่ซ้ายขวาด้านล่าง
        self.body_layout = QHBoxLayout()
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(0)
        self.main_layout.addLayout(self.body_layout)

        # --- [แก้ไขจุดที่ 2: เปลี่ยนจาก Sidebar Placeholder เป็น Sidebar คลาสจริง] ---
        self.sidebar = Sidebar(self)
        self.body_layout.addWidget(self.sidebar)

        # 4. พื้นที่เนื้อหาหลัก (Dynamic Content Stack)
        self.content_stack = QStackedWidget()
        self.body_layout.addWidget(self.content_stack)

        # ผูกลอจิกสัญญาณจากเมนูด้านข้าง (Signals and Slots) เข้ากับฟังก์ชันประมวลผล
        self.sidebar.menu_changed.connect(self.handle_menu_navigation)
        self.sidebar.logout_requested.connect(self.handle_logout)

        # เปิดวิวต้อนรับเริ่มต้น
        self.init_welcome_view()

    def init_welcome_view(self):
        self.welcome_label = QLabel(
            "ยินดีต้อนรับเข้าสู่ระบบงานสารบรรณและหมายจับ\n(เลือกเมนูด้านข้างเพื่อเริ่มต้นจัดการข้อมูล)"
        )
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet(
            "font-size: 18px; color: #555555; background-color: #FFFFFF;"
        )
        self.content_stack.addWidget(self.welcome_label)

    # --- [เพิ่มเติมจุดที่ 3: ฟังก์ชัน Slots สำหรับตอบสนองการกดเมนูและปุ่มออกจากระบบ] ---
    def handle_menu_navigation(self, menu_name):
        """รับสัญญาณการคลิกเมนูย่อยแล้วจำลองการเปลี่ยนหน้า"""
        # สเต็ปถัดๆ ไปเราจะสร้างหน้า View จริงมาแอดเข้าคลัง Stack ตรงนี้แทนข้อความชั่วคราวครับ
        temp_view = QLabel(
            f"กำลังเปิดหน้างาน: [{menu_name}]\n(ขณะนี้อยู่ระหว่างพัฒนาเนื้อหาในส่วนถัดไป)"
        )
        temp_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        temp_view.setStyleSheet(
            "font-size: 16px; color: #1A2B4C; background-color: #FFFFFF;"
        )

        # นำหน้าจอจำลองใส่ลงในแผงแสดงผลและสลับไปที่หน้าล่าสุดทันที
        self.content_stack.addWidget(temp_view)
        self.content_stack.setCurrentWidget(temp_view)

    def handle_logout(self):
        """ตรวจสอบและยืนยันสิทธิ์ก่อนทำลายเซสชันออกจากระบบ"""
        confirm = QMessageBox.question(
            self,
            "ยืนยันการออกจากระบบ",
            "คุณต้องการออกจากระบบงานตรวจสอบเอกสารใช่หรือไม่?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            print("ระบบทำการบันทึก Log และปิดแอปพลิเคชันอย่างปลอดภัย")
            self.close()
