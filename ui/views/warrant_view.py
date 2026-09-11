# ui/views/warrant_view.py
"""
Investigation Documents System - Warrant View (Filter View)
Features advanced suspect/warrant filtering tools and a comprehensive data table.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QHeaderView,
    QFormLayout,
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
import config


class WarrantView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 1. เลย์เอาต์หลักแนวตั้ง และเว้นระยะขอบสเปกทางการ
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 2. หัวข้อประจำหน้างาน (Page Header)
        header_label = QLabel("🗂️ ระบบค้นหาและบริหารจัดการข้อมูลหมายจับ (Warrant Filter View)")
        header_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #1A2B4C;"
        )
        main_layout.addWidget(header_label)

        # 3. แผงกล่องตัวกรองสืบค้นข้อมูล (Filter Group Box Container)
        filter_container = QWidget()
        filter_container.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #D2DCFF;
                border-radius: 6px;
            }
            QLineEdit { border: 1px solid #C4D1E0; }
        """)
        filter_main_layout = QVBoxLayout(filter_container)
        filter_main_layout.setContentsMargins(15, 15, 15, 15)

        # ใช้ Form Layout ในการจัดเรียงคู่ฟิลด์กรอกข้อมูลให้ซ้ายขวาตรงกันอย่างเป็นระเบียบ
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # สร้างฟิลด์กรอกตัวกรองหมายจับ
        self.warrant_no_input = QLineEdit()
        self.warrant_no_input.setPlaceholderText("ตัวอย่าง: 123/2569")

        self.suspect_name_input = QLineEdit()
        self.suspect_name_input.setPlaceholderText("ชื่อ หรือ นามสกุลของผู้ต้องหา")

        self.charge_input = QLineEdit()
        self.charge_input.setPlaceholderText("ข้อหา เช่น ลักทรัพย์, พรบ.ยาเสพติด")

        # บรรจุฟิลด์เข้าสู่ Form Layout
        form_layout.addRow(QLabel("เลขที่หมายจับ:"), self.warrant_no_input)
        form_layout.addRow(QLabel("ชื่อ-สกุล ผู้ต้องหา:"), self.suspect_name_input)
        form_layout.addRow(QLabel("ฐานความผิด/ข้อหา:"), self.charge_input)
        filter_main_layout.addLayout(form_layout)

        # 4. แถบปุ่มคำสั่งควบคุมการค้นหา (Action Buttons Layout)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.search_btn = QPushButton("🔍 ค้นหาข้อมูล")
        self.search_btn.setFixedWidth(120)
        self.search_btn.clicked.connect(self.execute_search)

        self.clear_btn = QPushButton("🔄 ล้างค่าตัวกรอง")
        self.clear_btn.setFixedWidth(120)
        self.clear_btn.setStyleSheet(
            "background-color: #7F8C8D; color: white;"
        )  # สีเทาเรียบร้อยสำหรับปุ่มล้างค่า
        self.clear_btn.clicked.connect(self.clear_filters)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.search_btn)
        filter_main_layout.addLayout(btn_layout)

        main_layout.addWidget(filter_container)

        # 5. ส่วนตารางแสดงผลรายชื่อผู้ต้องหาตามหมายจับ (QTableView)
        table_label = QLabel("📊 รายการข้อมูลผลการสืบค้นหมายจับผู้ต้องหา")
        table_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #1A2B4C; margin-top: 5px;"
        )
        main_layout.addWidget(table_label)

        self.table_view = QTableView()
        self.table_view.setMinimumHeight(350)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )  # เลือกไฮไลท์ทั้งแถวเมื่อคลิก

        # จัดตั้งโมเดลและหัวข้อหัวคอลัมน์ของตารางข้อมูล
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            [
                "เลขที่หมายจับ",
                "ศาลที่ออกหมาย",
                "ชื่อ-นามสกุลผู้ต้องหา",
                "ฐานความผิดความย่อ",
                "วันออกหมายจับ",
                "สถานะการจัดการ",
            ]
        )
        self.table_view.setModel(self.model)

        # ปรับขยายขนาดหัวคอลัมน์ตารางให้เต็มพื้นที่และยืดหยุ่นโดยอัตโนมัติ
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # โหลดข้อมูลจำลองผู้ต้องหาขึ้นมาแสดงผลทดสอบหน้าตาระบบ
        self.load_mock_warrants()
        main_layout.addWidget(self.table_view)

        # 6. เปิดระบบคีย์ลัด: สามารถกดปุ่ม Enter ในช่องกรอกใดก็ได้เพื่อเริ่มสั่งค้นหาข้อมูลทันที
        self.warrant_no_input.returnPressed.connect(self.execute_search)
        self.suspect_name_input.returnPressed.connect(self.execute_search)
        self.charge_input.returnPressed.connect(self.execute_search)

    def load_mock_warrants(self):
        """จำลองบันทึกข้อมูลหมายจับในระบบสารบรรณพนักงานสอบสวน"""
        self.mock_warrants_data = [
            [
                "มจ.145/2569",
                "ศาลจังหวัดชลบุรี",
                "นายสมชาย ใจกล้า",
                "ลักทรัพย์ในเวลากลางคืน",
                "10 ก.ย. 2569",
                "⚠️ ยังไม่พบตัว",
            ],
            [
                "มจ.202/2569",
                "ศาลจังหวัดชลบุรี",
                "นายอภิชาติ มาเยอะ",
                "ขับรถในขณะเมาสุรา",
                "05 ก.ย. 2569",
                "✅ จับกุมแล้ว",
            ],
            [
                "มจ.88/2569",
                "ศาลแขวงชลบุรี",
                "นางสาวสมศรี มีสุข",
                "เล่นการพนัน (ไฮโล)",
                "22 ส.ค. 2569",
                "⚠️ ยังไม่พบตัว",
            ],
            [
                "มจ.311/2569",
                "ศาลจังหวัดชลบุรี",
                "Mr. John Doe",
                "เป็นบุคคลต่างด้าวหลบหนีเข้าเมือง",
                "15 ส.ค. 2569",
                "❌ หมดอายุความ",
            ],
        ]
        self.display_data(self.mock_warrants_data)

    def display_data(self, data_list):
        """เติมรายการลงตารางและสั่งห้ามดับเบิ้ลคลิกแก้ไขค่าข้อมูลตรงๆ"""
        self.model.removeRows(0, self.model.rowCount())
        for row in data_list:
            items = [QStandardItem(field) for field in row]
            for item in items:
                item.setEditable(False)
            self.model.appendRow(items)

    def execute_search(self):
        """ลอจิกคัดกรองข้อมูลจำลองแบบเรียลไทม์จากตัวกรองที่พิมพ์"""
        w_no = self.warrant_no_input.text().strip().lower()
        s_name = self.suspect_name_input.text().strip().lower()
        charge = self.charge_input.text().strip().lower()

        filtered_result = []
        for row in self.mock_warrants_data:
            # ดึงค่าคอลัมน์ [0]=เลขหมายจับ, [2]=ชื่อผู้ต้องหา, [3]=ข้อหา
            match_no = w_no in row[0].lower() if w_no else True
            match_name = s_name in row[2].lower() if s_name else True
            match_charge = charge in row[3].lower() if charge else True

            if match_no and match_name and match_charge:
                filtered_result.append(row)

        self.display_data(filtered_result)

    def clear_filters(self):
        """ล้างค่าช่องป้อนข้อมูลทั้งหมดและสั่งรีเซ็ตคืนค่าตารางหลัก"""
        self.warrant_no_input.clear()
        self.suspect_name_input.clear()
        self.charge_input.clear()
        self.display_data(self.mock_warrants_data)
