# ui/views/case_view.py
"""
Investigation Documents System - Case View Module
Displays statistics for specific crime types (DUI, Drug, Gambling, Foreign)
and includes a structured, filterable investigation case table.
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
from ui.components.stat_card import StatCard


class CaseView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 1. เลย์เอาต์หลักแนวตั้ง
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 2. หัวข้อประจำหน้างาน (Page Header)
        header_label = QLabel(
            "⚖️ ระบบรายงานสถิติและบริหารจัดการสำนวนการสอบสวน (Case Management View)"
        )
        header_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #1A2B4C;"
        )
        main_layout.addWidget(header_label)

        # 3. แผงแสดงสถิติตัวเลขแยกตามประเภทคดีอาญา (Case Specific Stat Cards)
        # ดึงคู่สเปกสีประจำคดีจากข้อกำหนดในใบงาน UI DESIGN
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        self.card_dui = StatCard(
            "🚗 สถิติคดีเมาขับ", "142 คดี", config.CARD_DUI_BLUE, "white", self
        )
        self.card_drug = StatCard(
            "💊 สถิติคดียาเสพติด", "385 คดี", config.CARD_DRUG_GREEN, "white", self
        )
        self.card_gamble = StatCard(
            "🎲 สถิติคดีการพนัน", "64 คดี", config.CARD_GAMBLE_RED, "white", self
        )
        self.card_foreign = StatCard(
            "🛂 คดีต่างด้าว/ประจำรถ", "98 คดี", config.CARD_VEHICLE_ORANGE, "white", self
        )

        stats_layout.addWidget(self.card_dui)
        stats_layout.addWidget(self.card_drug)
        stats_layout.addWidget(self.card_gamble)
        stats_layout.addWidget(self.card_foreign)
        main_layout.addLayout(stats_layout)

        # 4. กล่องป้อนข้อมูลตัวกรองสืบค้นสำนวน (Case Filter Box)
        filter_container = QWidget()
        filter_container.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #D2DCFF;
                border-radius: 6px;
            }
        """)
        filter_layout = QVBoxLayout(filter_container)
        filter_layout.setContentsMargins(15, 12, 15, 12)

        form_layout = QFormLayout()
        form_layout.setSpacing(8)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.case_id_input = QLineEdit()
        self.case_id_input.setPlaceholderText("ตัวอย่าง: 450/2569")

        self.accused_input = QLineEdit()
        self.accused_input.setPlaceholderText("ชื่อ-นามสกุลของผู้ต้องหาในสำนวน")

        form_layout.addRow(QLabel("เลขรับคำร้องทุกข์/สำนวนคดี:"), self.case_id_input)
        form_layout.addRow(QLabel("ชื่อผู้ต้องหา/ผู้ถูกกล่าวหา:"), self.accused_input)
        filter_layout.addLayout(form_layout)

        # ปุ่มคำสั่งค้นหาสำนวน
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        btn_layout.setSpacing(10)

        self.clear_btn = QPushButton("🔄 รีเซ็ต")
        self.clear_btn.setFixedWidth(100)
        self.clear_btn.setStyleSheet("background-color: #7F8C8D; color: white;")
        self.clear_btn.clicked.connect(self.clear_case_filters)

        self.search_btn = QPushButton("🔍 ค้นหาสำนวน")
        self.search_btn.setFixedWidth(120)
        self.search_btn.clicked.connect(self.execute_case_search)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.search_btn)
        filter_layout.addLayout(btn_layout)

        main_layout.addWidget(filter_container)

        # 5. ตารางแสดงผลรายชื่อสำนวนการสอบสวน (Case Data Table)
        table_label = QLabel("📋 รายการแฟ้มสำนวนการสอบสวนในความรับผิดชอบ")
        table_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #1A2B4C; margin-top: 5px;"
        )
        main_layout.addWidget(table_label)

        self.table_view = QTableView()
        self.table_view.setMinimumHeight(280)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            [
                "เลขสำนวนคดี",
                "ประเภทฐานความผิด",
                "ชื่อผู้ต้องหา",
                "พนักงานสอบสวนผู้รับผิดชอบ",
                "สถานะสำนวน",
                "ความคืบหน้า",
            ]
        )
        self.table_view.setModel(self.model)

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # โหลดข้อมูลจำลองสำนวนคดีขึ้นมาแสดงผลทดสอบหน้าตาระบบ
        self.load_mock_cases()
        main_layout.addWidget(self.table_view)

        # 6. คีย์ลัดกด Enter เพื่อสั่งค้นหาสำนวนได้ทันที
        self.case_id_input.returnPressed.connect(self.execute_case_search)
        self.accused_input.returnPressed.connect(self.execute_case_search)

    def load_mock_cases(self):
        """จำลองบันทึกข้อมูลสารบบสำนวนคดีอาญาตามประเภทในข้อกำหนด"""
        self.mock_cases_data = [
            [
                "สว.450/2569",
                "ขับรถในขณะเมาสุรา (เมาขับ)",
                "นายมานะ เดินดี",
                "พ.ต.ท. วรนันท์",
                "คดีเสร็จสิ้น",
                "ส่งพนักงานอัยการแล้ว",
            ],
            [
                "สว.451/2569",
                "เสพสารเสพติดให้โทษ (เสพ)",
                "นายวิชัย ไวไว",
                "ร.ต.อ. สมชาย",
                "อยู่ระหว่างสอบสวน",
                "รอผลตรวจพิสูจน์สารเสพติด",
            ],
            [
                "สว.452/2569",
                "ลักลอบเล่นการพนัน (การพนัน)",
                "นางใจดี มีทรัพย์",
                "พ.ต.ท. วรนันท์",
                "คดีเสร็จสิ้น",
                "ศาลมีคำพิพากษาแล้ว",
            ],
            [
                "สว.453/2569",
                "เป็นบุคคลต่างด้าวทำงานหลบหนี (ต่างด้าว)",
                "Mr. Somba",
                "ร.ต.ท. หญิง ดวงใจ",
                "อยู่ระหว่างสอบสวน",
                "ควบคุมตัวรอผลผลักดันออก",
            ],
        ]
        self.display_cases(self.mock_cases_data)

    def display_cases(self, data_list):
        self.model.removeRows(0, self.model.rowCount())
        for row in data_list:
            items = [QStandardItem(field) for field in row]
            for item in items:
                item.setEditable(False)
            self.model.appendRow(items)

    def execute_case_search(self):
        """ลอจิกคัดกรองข้อมูลสำนวนคดีจากฟิลด์คำค้นหา"""
        c_id = self.case_id_input.text().strip().lower()
        accused = self.accused_input.text().strip().lower()

        filtered = []
        for row in self.mock_cases_data:
            match_id = c_id in row[0].lower() if c_id else True
            match_name = accused in row[2].lower() if accused else True

            if match_id and match_name:
                filtered.append(row)
        self.display_cases(filtered)

    def clear_case_filters(self):
        self.case_id_input.clear()
        self.accused_input.clear()
        self.display_cases(self.mock_cases_data)
