# ui/views/home_view.py (ฉบับแก้ไขจัดการลำดับการเข้าถึงฐานข้อมูล)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
import config
from ui.components.stat_card import StatCard
from database.services import InvestigationService


class HomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 📌 1. ย้ายชุดคำสั่งคิวรี่สถิติจากเดิมที่เคยอยู่นอกคลาส เข้ามาอยู่ด้านในฟังก์ชันนี้อย่างปลอดภัย
        total_w, captured_w, uncaptured_w = InvestigationService.get_dashboard_counts()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        header_label = QLabel("แผงควบคุมระบบและสรุปข้อมูลสารสนเทศ (Dashboard)")
        header_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #1A2B4C;"
        )
        main_layout.addWidget(header_label)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        # ประกอบข้อมูลตัวแปรตัวเลขจริงจากการคิวรี่ฐานข้อมูล
        self.card_total = StatCard(
            "📊 ยอดรวมหมายจับทั้งหมด",
            f"{total_w} หมาย",
            config.CARD_TOTAL_BLUE,
            "white",
            self,
        )
        self.card_captured = StatCard(
            "✅ จับกุม/ถอนหมายแล้ว",
            f"{captured_w} หมาย",
            config.CARD_SUCCESS_GREEN,
            "white",
            self,
        )
        self.card_pending = StatCard(
            "⚠️ หมายจับคงเหลือ (ระวังเหตุ)",
            f"{uncaptured_w} หมาย",
            config.CARD_WARNING_YELLOW,
            "#4A3B00",
            self,
        )

        cards_layout.addWidget(self.card_total)
        cards_layout.addWidget(self.card_captured)
        cards_layout.addWidget(self.card_pending)
        main_layout.addLayout(cards_layout)

        # ตารางประวัติกิจกรรม (คงเดิม)
        activity_label = QLabel("📋 ประวัติการทำรายการล่าสุดในระบบ")
        activity_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #1A2B4C; margin-top: 10px;"
        )
        main_layout.addWidget(activity_label)

        self.tree_view = QTreeView()
        self.tree_view.setMinimumHeight(350)
        self.tree_view.setRootIsDecorated(False)
        self.tree_view.setAlternatingRowColors(True)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            ["ลำดับ", "กิจกรรม/ความเคลื่อนไหวระบบ", "วันที่", "เวลา", "ผู้ปฏิบัติหน้าที่"]
        )
        self.tree_view.setModel(self.model)

        self.load_mock_activities()
        main_layout.addWidget(self.tree_view)

    def load_mock_activities(self):
        mock_data = [
            [
                "1",
                "ระบบเปิดใช้งานการเชื่อมต่อฐานข้อมูล SQLite สำเร็จ",
                "11 ก.ย. 2569",
                "21:00",
                "ระบบอัตโนมัติ",
            ],
            [
                "2",
                "สืบค้นข้อมูลหมายจับผู้ต้องหาคดีลักทรัพย์",
                "11 ก.ย. 2569",
                "20:45",
                "พ.ต.ท. วรนันท์",
            ],
        ]
        for row in mock_data:
            items = [QStandardItem(field) for field in row]
            for item in items:
                item.setEditable(False)
            self.model.appendRow(items)
