# database/services.py (ฉบับแก้ไขระบบยืนยันสิทธิ์ความปลอดภัย)
"""
Investigation Documents System - Service Layer
Acts as the controller between UI widgets and the SQLAlchemy Database Manager.
"""

from database.connection import SessionLocal, User, Warrant, CaseFile, SystemLog
import datetime


# database/services.py (ฉบับแก้ไขสิทธิ์แก้บั๊ก DetachedInstanceError)


# database/services.py (ฉบับแก้ไขระบบ Commit และล้างบั๊ก DetachedInstanceError อย่างเด็ดขาด)


class InvestigationService:
    @staticmethod
    def authenticate_user(username, password):
        """ตรวจสอบสิทธิ์การเข้าใช้งาน พร้อมทำระบบ Refresh ข้อมูลกลับเข้าสู่แรมหลังการ Commit อย่างปลอดภัย"""
        db = SessionLocal()
        try:
            # คิวรี่หาข้อมูลผู้ใช้งานจากตารางจริง
            user = (
                db.query(User)
                .filter(User.username == username, User.password_hash == password)
                .first()
            )

            if user:
                # 1. จัดทำและบันทึกประวัติกิจกรรม Logs ลงตารางฐานข้อมูลตามข้อกำหนดที่ 5
                log_details = (
                    f"ผู้ใช้งาน {user.rank_title}{user.first_name} ลงชื่อเข้าสู่ระบบสำเร็จ"
                )
                new_log = SystemLog(action_details=log_details, user_id=user.user_id)
                db.add(new_log)

                # ⚠️ จุดสำคัญ: เมื่อสั่ง commit ข้อมูล อ็อบเจกต์ user จะถูกสั่งล้างค่าสถานะ (Expired) อัตโนมัติ
                db.commit()

                # 📌 วิธีแก้ไขที่ถูกต้อง: สั่งดึงข้อมูล ยศ และ ชื่อ กลับเข้ามาล็อกเก็บไว้ในแรมใหม่อีกครั้งทันที
                db.refresh(user)

                # ทำการคัดลอก (Detach/Expunge) อ็อบเจกต์ออกมาเป็นอิสระ เพื่อให้ UI นำไปแกะค่าใช้งานต่อได้แม้จะสั่ง db.close() ไปแล้ว
                db.expunge(user)

                return user

            return None
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการตรวจสอบสิทธิ์: {e}")
            return None
        finally:
            db.close()  # ปิดการเชื่อมต่อฐานข้อมูลได้อย่างปลอดภัย ข้อมูลในแรมไม่หาย

    @staticmethod
    def get_dashboard_counts():
        """นับจำนวนสถิติสรุปงานบนหน้าแดชบอร์ด"""
        db = SessionLocal()
        try:
            total = db.query(Warrant).count()
            captured = db.query(Warrant).filter(Warrant.status == "จับกุมแล้ว").count()
            uncaptured = db.query(Warrant).filter(Warrant.status == "ยังไม่พบตัว").count()
            return total, captured, uncaptured
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการดึงสถิติแดชบอร์ด: {e}")
            return 0, 0, 0
        finally:
            db.close()
