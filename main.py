# main.py
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.views.login_view import LoginView
from ui.styles import get_global_stylesheet
from database.connection import init_database  # นำเข้าฟังก์ชันเตรียมระบบตารางคดี


class AppController:
    def __init__(self):
        self.login_window = None
        self.main_window = None

    def show_login(self):
        self.login_window = LoginView()
        self.login_window.setWindowTitle("ลงชื่อเข้าใช้งานระบบงานหมายจับ")
        self.login_window.resize(500, 450)
        self.login_window.login_success.connect(self.start_main_application)
        self.login_window.show()

    def start_main_application(self, username):
        self.main_window = MainWindow()
        self.main_window.show()
        if self.login_window:
            self.login_window.close()
            self.login_window = None


def main():
    # 📌 บรรทัดสำคัญที่สุด: ต้องสั่งสร้างตารางและใส่ Seed Data ลงไฟล์ .db ก่อนการเรียกประมวลผลส่วนดีไซน์หน้าจอเสมอ
    init_database()

    app = QApplication(sys.argv)
    app.setStyleSheet(get_global_stylesheet())

    controller = AppController()
    controller.show_login()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
