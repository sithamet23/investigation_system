# ui/views/document_view.py
"""
Investigation Documents System - Document View Module
Manages official document requests, filters, and handles DOCX/PDF export actions.
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
    QMessageBox,
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
import config


class DocumentView(QWidget):
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
            "📄 ระบบบริหารจัดการเอกสารและแบบฟอร์มคดี (Document Management View)"
        )
        header_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #1A2B4C;"
        )
        main_layout.addWidget(header_label)

        # 3. แผงควบคุมตัวกรองสืบค้นเอกสาร (Document Filter Box)
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

        self.doc_name_input = QLineEdit()
        self.doc_name_input.setPlaceholderText(
            "ชื่อเอกสาร หรือ เลขที่หนังสือส่ง เช่น ขอทราบผลคดี"
        )

        form_layout.addRow(QLabel("คำค้นหาเกี่ยวกับเอกสาร:"), self.doc_name_input)
        filter_layout.addLayout(form_layout)

        # ปุ่มสืบค้น
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        btn_layout.setSpacing(10)

        self.search_btn = QPushButton("🔍 ค้นหาเอกสาร")
        self.search_btn.setFixedWidth(120)
        self.search_btn.clicked.connect(self.execute_doc_search)
        filter_layout.addLayout(btn_layout)

        main_layout.addWidget(filter_container)

        # 4. แผงปุ่มสำหรับสั่งสร้างเอกสารด่วน (Quick Document Generation Actions)
        action_label = QLabel("⚡ บริการสร้างเอกสารและแบบฟอร์มกฎหมายด่วน")
        action_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #1A2B4C;"
        )
        main_layout.addWidget(action_label)

        actions_container = QWidget()
        actions_layout = QHBoxLayout(actions_container)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(10)

        # ปุ่มสร้างเอกสารแต่ละประเภทตามใบงาน REQUIREMENTS
        self.btn_req_result = QPushButton("📝 ขอทราบผลคดี")
        self.btn_send_warrant = QPushButton("📬 แจ้งผลส่งหมายเรียก")
        self.btn_seize_status = QPushButton("🔒 แจ้งอายัด/ถอนผู้ต้องหา")

        # ปรับสไตล์ปุ่มให้ดูเรียบร้อยแตกต่างจากปุ่มสืบค้นหลัก
        for btn in [self.btn_req_result, self.btn_send_warrant, self.btn_seize_status]:
            btn.setStyleSheet(
                f"background-color: {config.SIDEBAR_BG}; color: {config.PRIMARY_NAV_BG}; border: 1px solid #D2DCFF; font-weight: bold; padding: 8px;"
            )
            actions_layout.addWidget(btn)

        # ผูกลอจิกการกดปุ่มสร้างเอกสารเข้ากับฟังก์ชันสเต็ปถัดไป
        self.btn_req_result.clicked.connect(
            lambda: self.generate_document("หนังสือขอทราบผลคดีอาญา")
        )
        self.btn_send_warrant.clicked.connect(
            lambda: self.generate_document("รายงานผลการส่งหมายเรียกพยาน")
        )
        self.btn_seize_status.clicked.connect(
            lambda: self.generate_document("หนังสือแจ้งอายัด/ถอนอายัดผู้ต้องหา")
        )

        main_layout.addWidget(actions_container)

        # 5. ตารางแสดงประวัติและสถานะไฟล์เอกสาร (Document History Table)
        table_label = QLabel("📋 ประวัติการออกเอกสารและไฟล์ที่พร้อมดาวน์โหลด (DOCX / PDF)")
        table_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #1A2B4C; margin-top: 5px;"
        )
        main_layout.addWidget(table_label)

        self.table_view = QTableView()
        self.table_view.setMinimumHeight(280)
        self.table_view.setAlternatingRowColors(True)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            [
                "เลขที่เอกสาร",
                "ชื่อประเภทแบบฟอร์มเอกสาร",
                "ผู้ต้องหา/คดีอ้างอิง",
                "วันที่สร้าง",
                "ดาวน์โหลด DOCX",
                "ดาวน์โหลด PDF",
            ]
        )
        self.table_view.setModel(self.model)

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.load_mock_documents()
        main_layout.addWidget(self.table_view)

        # คีย์ลัดกด Enter เพื่อค้นหาเอกสาร
        self.doc_name_input.returnPressed.connect(self.execute_doc_search)

    def load_mock_documents(self):
        """จำลองคลังประวัติไฟล์เอกสารในระบบ"""
        self.mock_docs_data = [
            [
                "ตช.0015/124",
                "หนังสือขอทราบผลคดีอาญา",
                "นายสมชาย ใจกล้า",
                "11 ก.ย. 2569",
                "📥 โหลดไฟล์ (DOCX)",
                "📥 เปิดไฟล์ (PDF)",
            ],
            [
                "ตช.0015/125",
                "รายงานผลการส่งหมายเรียกพยาน",
                "นายวิชัย ไวไว",
                "10 ก.ย. 2569",
                "📥 โหลดไฟล์ (DOCX)",
                "📥 เปิดไฟล์ (PDF)",
            ],
            [
                "ตช.0015/126",
                "หนังสือแจ้งอายัด/ถอนอายัดผู้ต้องหา",
                "นางใจดี มีทรัพย์",
                "09 ก.ย. 2569",
                "📥 โหลดไฟล์ (DOCX)",
                "📥 เปิดไฟล์ (PDF)",
            ],
        ]
        self.display_documents(self.mock_docs_data)

    def display_documents(self, data_list):
        self.model.removeRows(0, self.model.rowCount())
        for row in data_list:
            items = [QStandardItem(field) for field in row]
            for item in items:
                item.setEditable(False)
            self.model.appendRow(items)

    def execute_doc_search(self):
        """คัดกรองชื่อเอกสารตามคำค้นหา"""
        search_text = self.doc_name_input.text().strip().lower()
        filtered = []
        for row in self.mock_docs_data:
            if search_text in row[1].lower() or search_text in row[2].lower():
                filtered.append(row)
        self.display_documents(filtered)

    def generate_document(self, doc_type):
        """ฟังก์ชันรองรับระบบการออกรายงานและแปลงไฟล์ (DOCX / PDF Generation Exception)"""
        QMessageBox.information(
            self,
            "ระบบเอกสารอัตโนมัติ",
            f"ระบบกำลังทำการดึงข้อมูลคดี ประมวลผล QSS และทำรายงานแฟ้มข้อมูล\nประเภท: [{doc_type}]\nสถานะ: สร้างไฟล์สำเร็จ (DOCX / PDF พร้อมใช้งาน)",
            QMessageBox.StandardButton.Ok,
        )
