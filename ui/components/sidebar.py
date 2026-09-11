from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal
import config
from ui.styles import get_sidebar_stylesheet


class Sidebar(QWidget):
    # สร้าง Custom Signals สำหรับแจ้งเตือนหน้าต่างหลักเมื่อเจ้าหน้าที่คลิกสลับเมนู
    menu_changed = pyqtSignal(str)  # ส่งชื่อหน้าจอ เช่น "Dashboard", "ค้นหาข้อมูลหมายจับ"
    logout_requested = pyqtSignal()  # ส่งสัญญาณเมื่อกดปุ่มออกจากระบบ

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)  # กำหนดความกว้างคงที่ตามใบงานออกแบบ UI
        self.menu_groups = {}  # สำหรับเก็บอ้างอิง {หัวข้อหลัก: [รายการปุ่มย่อย, Container]}
        self.all_sub_buttons = []  # เก็บปุ่มย่อยทั้งหมดเพื่อใช้ทำระบบค้นหา (Filter)
        self.init_ui()

    def init_ui(self):
        # 1. ติดตั้งสไตล์เฉพาะของ Sidebar
        self.setStyleSheet(get_sidebar_stylesheet())

        # 2. เลย์เอาต์หลักของ Sidebar (แนวตั้ง)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # จัดสไตล์กรอบแผงควบคุมด้านข้าง
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("SidebarFrame")
        frame_layout = QVBoxLayout(self.sidebar_frame)
        frame_layout.setContentsMargins(10, 15, 10, 15)
        frame_layout.setSpacing(10)
        main_layout.addWidget(self.sidebar_frame)

        # 3. โซนที่ 1: ช่องค้นหาเมนู (Instant Search View) ช่วยสืบค้นเมนูย่อยแบบเรียลไทม์
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 ค้นหาเมนูใช้งาน...")
        self.search_input.textChanged.connect(self.filter_menus)  # ผูกลอจิกพิมพ์ค้นหา
        frame_layout.addWidget(self.search_input)

        # 4. โซนที่ 2: พื้นที่เมนูนำทาง (Scroll Area รองรับกรณีเปิดกลุ่มเมนูยาวเกินหน้าจอ)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        self.menu_layout = QVBoxLayout(scroll_content)
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout.setSpacing(2)
        self.menu_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # เริ่มสร้างโครงสร้างเมนูตามข้อกำหนด REQUIREMENTS
        self.create_accordion_menus()

        scroll_area.setWidget(scroll_content)
        frame_layout.addWidget(scroll_area)

        # Spacer ดันปุ่ม Logout ให้ลงไปอยู่ล่างสุดเสมอ
        frame_layout.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # 5. โซนที่ 3: ปุ่ม Logout คงที่อยู่บริเวณด้านล่างสุด (Fixed Area)
        self.logout_btn = QPushButton("🚪 ออกจากระบบ")
        self.logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.DANGER_LOGOUT_RED};
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 10px;
            }}
            QPushButton:hover {{ background-color: #C9302C; }}
        """)
        self.logout_btn.clicked.connect(self.logout_requested.emit)
        frame_layout.addWidget(self.logout_btn)

    def create_accordion_menus(self):
        """โครงสร้างเมนูตามสเปกงานหมายจับ สารบรรณ และสำนวนการสอบสวน"""
        menu_structure = {
            "หน้าแรก": ["Dashboard"],
            "งานหมายจับ": ["ค้นหาข้อมูลหมายจับ", "บัญชีคุมหมายจับ", "บัญชีคุมอายัด", "บัญชีถอนหมายจับ"],
            "งานเอกสาร": [
                "ค้นหาเอกสาร",
                "ขอทราบผลคดี",
                "แจ้งผลคดี",
                "แจ้งผลการส่งหมายเรียก",
                "แจ้งอายัด/ถอนอายัดผู้ต้องหา",
                "ขอถอนหมายจับ",
            ],
            "สำนวนการสอบสวน": [
                "ค้นหาสำนวนคดี",
                "เมาขับ",
                "เสพ",
                "การพนัน",
                "ผู้ประจำรถ",
                "ต่างด้าว",
            ],
            "ข้อมูลระบบ": [
                "ข้อมูลผู้ต้องหา",
                "ข้อมูลพนักงานสอบสวน",
                "ข้อมูลผู้จับกุม",
                "สร้าง User",
                "กำหนดสิทธิ์",
            ],
        }

        for header_text, sub_menus in menu_structure.items():
            # สร้างปุ่มหัวข้อหลัก (Header)
            header_btn = QPushButton(header_text)
            header_btn.setProperty("class", "MenuHeader")
            self.menu_layout.addWidget(header_btn)

            # Container สำหรับเก็บปุ่มเมนูย่อยของแต่ละกลุ่ม
            sub_container = QWidget()
            container_layout = QVBoxLayout(sub_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(1)

            sub_buttons_list = []
            for sub_text in sub_menus:
                sub_btn = QPushButton(f"• {sub_text}")
                sub_btn.setProperty("class", "SubMenuBtn")
                # ผูกเหตุการณ์คลิกเข้ากับฟังก์ชันสลับหน้าจอ
                sub_btn.clicked.connect(
                    lambda checked, text=sub_text: self.menu_changed.emit(text)
                )

                container_layout.addWidget(sub_btn)
                sub_buttons_list.append(sub_btn)
                self.all_sub_buttons.append(
                    (sub_text, sub_btn, sub_container, header_btn)
                )

            self.menu_layout.addWidget(sub_container)
            self.menu_groups[header_btn] = sub_container

            # ผูกลอจิกการกดปุ่ม Header เพื่อซ่อน/แสดง Accordion Container
            header_btn.clicked.connect(
                lambda checked, c=sub_container: self.toggle_group(c)
            )

    def toggle_group(self, container):
        """ทำหน้าที่สลับสถานะ ซ่อน/แสดง เมนูย่อย (Accordion Workflow)"""
        container.setVisible(not container.isVisible())

    def filter_menus(self, text):
        """ระบบค้นหาคำแบบเรียลไทม์ (Instant Filter Search)"""
        search_text = text.strip().lower()

        # ค้นหาและซ่อน/แสดงปุ่มตามคำค้นหา
        for sub_text, sub_btn, container, header_btn in self.all_sub_buttons:
            if search_text in sub_text.lower():
                sub_btn.setVisible(True)
                container.setVisible(True)  # ขยายกลุ่มเมนูอัตโนมัติหากเจอคำค้นหา
            else:
                sub_btn.setVisible(False)

        # ซ่อนกลุ่มเมนูหลักหลัก (Header) หากไม่มีเมนูย่อยใดๆ ตรงกับคำค้นหาเลย
        for header, container in self.menu_groups.items():
            # ตรวจสอบว่าในคอนเทนเนอร์นี้มีปุ่มย่อยที่เปิดแสดงอยู่ไหม
            has_visible_child = any(
                child.isVisible() for child in container.findChildren(QPushButton)
            )
            header.setVisible(has_visible_child if search_text else True)
            if not search_text:
                container.setVisible(True)  # แสดงผลปกติแบบขยายทั้งหมดเมื่อช่องค้นหาว่าง
