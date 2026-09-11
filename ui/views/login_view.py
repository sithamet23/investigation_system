from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSignal
import config
from database.services import InvestigationService


class LoginView(QWidget):
    # สัญญาณแจ้งเตือนเมื่อผ่านการตรวจสอบสิทธิ์ (ส่งยศ-ชื่อผู้ใช้งานกลับไป)
    login_success = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 1. เลย์เอาต์หลักแนวตั้ง และตั้งสีพื้นหลังให้สอดคล้องกับธีมหลัก
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"background-color: {config.MAIN_CONTENT_BG};")

        # 2. กล่องฟอร์มลงชื่อเข้าใช้ (Login Container Box)
        form_widget = QWidget()
        form_widget.setFixedWidth(400)
        form_widget.setStyleSheet(f"""
            QWidget {{
                background-color: #FFFFFF;
                border: 1px solid #D2DCFF;
                border-radius: 8px;
            }}
        """)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(30, 40, 30, 40)
        form_layout.setSpacing(15)

        # หัวข้อและไอคอนระบบ
        title_icon = QLabel("⚖️")
        title_icon.setStyleSheet("font-size: 36px; border: none;")
        title_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(config.APP_NAME)
        title_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #1A2B4C; border: none;"
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 3. ช่องกรอกข้อมูลบัญชีผู้ใช้
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("ชื่อผู้ใช้งาน (Username)")
        self.username_input.setMinimumHeight(35)
        # ตัวอย่าง Username เริ่มต้นเพื่อความสะดวกรวดเร็วในการกดทดสอบระบบ
        self.username_input.setText("voranan_s")

        # ช่องกรอกรหัสผ่าน
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("รหัสผ่าน (Password)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # ซ่อนรหัสผ่านเป็นจุดดำ
        self.password_input.setMinimumHeight(35)

        # 4. ปุ่มกดยืนยันการเข้าสู่ระบบ
        self.login_btn = QPushButton("🔓 เข้าสู่ระบบ")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.PRIMARY_NAV_BG};
                color: white;
                font-weight: bold;
                border-radius: 4px;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: #243D6C; }}
        """)

        # ผูกฟังก์ชันการคลิกปุ่มเข้ากับระบบตรวจสอบรหัสผ่าน
        self.login_btn.clicked.connect(self.check_authentication)

        # เพิ่มองค์ประกอบเข้าในฟอร์มตามลำดับ
        form_layout.addWidget(title_icon)
        form_layout.addWidget(title_label)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_btn)

        main_layout.addWidget(form_widget)

        # 5. เปิดระบบคีย์ลัด: หากกดปุ่ม Enter บนแป้นพิมพ์ในหน้านี้จะเทียบเท่ากับการกดปุ่มเข้าสู่ระบบทันที
        self.username_input.returnPressed.connect(self.check_authentication)
        self.password_input.returnPressed.connect(self.check_authentication)

    # ui/views/login_view.py (จุดตรวจเช็คในฟังก์ชัน check_authentication)

    def check_authentication(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        # เรียกยืนยันสิทธิ์ผ่านบริการหลัก
        user = InvestigationService.authenticate_user(username, password)

        if user:
            # 📌 ดึงค่าแกะจาก SQLAlchemy Object ตรงๆ ตามฟิลด์ rank_title และ first_name
            fullname = f"{user.rank_title} {user.first_name}"
            print(f"ยืนยันสิทธิ์สำเร็จ: {fullname}")
            self.login_success.emit(fullname)
        else:
            QMessageBox.warning(
                self,
                "ข้อมูลไม่ถูกต้อง",
                "ชื่อผู้ใช้งานหรือรหัสผ่านระบบไม่ถูกต้อง",
                QMessageBox.StandardButton.Ok,
            )
