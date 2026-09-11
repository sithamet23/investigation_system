import config


def get_global_stylesheet():
    """ส่งคืนสไตล์ชีทรวมของแอปพลิเคชันสำหรับกำหนดค่าให้ QApplication"""
    return f"""
        /* กำหนดฟอนต์มาตรฐานและสีพื้นหลังของหน้าจอหลัก */
        QWidget {{
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_BASE}px;
        }}
        
        QMainWindow {{
            background-color: {config.MAIN_CONTENT_BG};
        }}

        /* ปุ่มกดมาตรฐาน (Action Buttons) */
        QPushButton {{
            background-color: {config.PRIMARY_NAV_BG};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
            min-height: 24px;
        }}
        QPushButton:hover {{
            background-color: #243D6C; /* สี Navy ที่สว่างขึ้นเล็กน้อยเมื่อ Hover */
        }}
        QPushButton:pressed {{
            background-color: #121F37;
        }}

        /* ช่องกรอกข้อมูล (Line Edit / Search Fields) */
        QLineEdit {{
            background-color: white;
            border: 1px solid #C4D1E0;
            border-radius: 4px;
            padding: 4px 8px;
            color: #333333;
        }}
        QLineEdit:focus {{
            border: 1px solid {config.CARD_TOTAL_BLUE};
        }}

        /* ตารางแสดงผลข้อมูล (Table View / Tree View สำหรับบันทึกหมายจับและสำนวน) */
        QTableView, QTreeView {{
            background-color: white;
            border: 1px solid #D2DCFF;
            gridline-color: #E2EAF4;
            selection-background-color: #E3EDFB;
            selection-color: #1A2B4C;
            alternate-background-color: #F8FAFC;
        }}
        QHeaderView::section {{
            background-color: {config.SIDEBAR_BG};
            color: #1A2B4C;
            padding: 6px;
            border: 1px solid #D2DCFF;
            font-weight: bold;
        }}
    """


def get_sidebar_stylesheet():
    """สไตล์เฉพาะสำหรับ Accordion Sidebar เมนูด้านข้าง"""
    return f"""
        QFrame#SidebarFrame {{
            background-color: {config.SIDEBAR_BG};
            border-right: 1px solid #D2DCFF;
        }}
        /* ปุ่มเมนูหลักใน Accordion */
        QPushButton.MenuHeader {{
            background-color: #DDE5EE;
            color: {config.PRIMARY_NAV_BG};
            text-align: left;
            padding: 8px 12px;
            font-weight: bold;
            border-bottom: 1px solid #CBD7E5;
            border-radius: 0px;
        }}
        QPushButton.MenuHeader:hover {{
            background-color: #D1DCE9;
        }}
        /* ปุ่มเมนูย่อยข้างใน Accordion */
        QPushButton.SubMenuBtn {{
            background-color: transparent;
            color: #4A5568;
            text-align: left;
            padding: 6px 24px;
            border-radius: 0px;
        }}
        QPushButton.SubMenuBtn:hover {{
            background-color: #E2E8F0;
            color: {config.PRIMARY_NAV_BG};
        }}
    """
