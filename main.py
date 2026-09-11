import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.styles import get_global_stylesheet


def main():
    # สร้างอินสแตนซ์หลักของระบบแอปพลิเคชัน
    app = QApplication(sys.argv)

    # ดึงค่าสไตล์ชีทส่วนกลางที่เราออกแบบตามหลักราชการมาติดตั้งให้กับตัวแอป
    app.setStyleSheet(get_global_stylesheet())

    # เปิดหน้าต่างโปรแกรมหลักขึ้นมาแสดงผล
    window = MainWindow()
    window.show()

    # รันลูปของระบบตามสถาปัตยกรรมของ PyQt6
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
