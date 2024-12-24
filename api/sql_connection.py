import pymysql
import json

class SqlAPI:
    def __init__(self ):
        """
        讀取 sql_config.json 內參數進行連接

        """
        try:
            with open("sql_config.json", 'r') as file:
                config = json.load(file)

            self.connection = pymysql.connect(
                host=config["host"],
                user=config["username"],
                port=config["port"],
                password=config["password"],
                database=config["database"]
            )
            self.cursor = self.connection.cursor()
            print("資料庫連線成功！")
        except (pymysql.MySQLError, FileNotFoundError, KeyError) as e:

            print(f"資料庫連線失敗或配置檔案錯誤: {e}")

    def is_valid_roc_id(id_num):
        """
        驗證中華民國身份證字號是否合法
        :param id_num: 身份證字號
        :return: True 合法, False 不合法
        """
        if len(id_num) != 10 or not id_num[0].isalpha() or not id_num[1:].isdigit():
            return False

        # 第一個字母轉換為數字
        first_letter = id_num[0].upper()
        if not ('A' <= first_letter <= 'Z'):
            return False

        # 使用 ASCII Code 與 Offset 計算
        ascii_offset = ord(first_letter) - 65  # 'A' 的 ASCII 是 65
        converted_letter = 10 + ascii_offset  # 對應的數字：A -> 10, B -> 11, ..., Z -> 33

        if first_letter == 'I':  # 特殊處理 I -> 34
            converted_letter = 34
        elif first_letter == 'O':  # 特殊處理 O -> 35
            converted_letter = 35

        # 計算檢查碼
        total = (converted_letter // 10) + (converted_letter % 10) * 9
        for i, digit in enumerate(id_num[1:9]):
            total += int(digit) * (8 - i)
        total += int(id_num[-1])  # 加上最後一碼

        return total % 10 == 0

    def userreg(self, id_num, name, phone, email, password, address, user_type, **kwargs):
        """
        註冊新用戶。
        :param id_num: 身份證字號
        :param name: 中文名
        :param phone: 電話號碼
        :param email: email
        :param password: 密碼
        :param address: 住址
        :param user_type: 使用者類型 ('admin', 'rater', 'student', 'teacher')
        :param kwargs: 額外的參數
        :return: 註冊結果訊息
        資料庫內已對 身份證號丶email丶電話設置 unique，判斷重複註冊無需在python內處理

        """
        try:
            # 驗證身份證字號合法性
            if not SqlAPI.is_valid_roc_id(id_num):
                return "身份證字號不合法，請確認後重新輸入。"

            # 基本插入查詢
            base_query = """
            INSERT INTO `user` (ID_num, name, phone, email, password, address, is_admin, is_rater, is_student, is_teacher, admin_type, rater_title, s_t_id, t_t_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # 根據使用者類型設置對應的值
            is_admin = 1 if user_type == "admin" else 0
            is_rater = 1 if user_type == "rater" else 0
            is_student = 1 if user_type == "student" else 0
            is_teacher = 1 if user_type == "teacher" else 0

            admin_type = kwargs.get("admin_type", None)
            rater_title = kwargs.get("rater_title", None)
            s_t_id = kwargs.get("s_t_id", None)
            t_t_id = kwargs.get("t_t_id", None)

            # 執行插入
            self.cursor.execute(
                base_query,
                (
                    id_num,
                    name,
                    phone,
                    email,
                    password,
                    address,
                    is_admin,
                    is_rater,
                    is_student,
                    is_teacher,
                    admin_type,
                    rater_title,
                    s_t_id,
                    t_t_id,
                ),
            )
            self.connection.commit()
            return "用戶註冊成功！"

        except pymysql.IntegrityError as e:
            # 處理唯一性約束錯誤
            if "Duplicate entry" in str(e):
                if "ID_num" in str(e):
                    return "身份證字號已存在，請確認或使用其他身份證字號。"
                elif "phone" in str(e):
                    return "電話號碼已存在，請確認或使用其他電話號碼。"
                elif "email" in str(e):
                    return "電子郵件已存在，請確認或使用其他電子郵件。"
            return f"註冊失敗: {e}"

        except pymysql.MySQLError as e:
            # 處理其他 SQL 錯誤
            self.connection.rollback()
            return f"註冊失敗: {e}"

    def userchangepassword(self, u_id, old_password, new_password):
        """
        使用者已知密碼情況下改密碼。
        :param u_id: user id
        :param old_password: 原密碼
        :param new_password: 新密碼
        :return: 成功if成功 or 失敗if老密碼錯誤

        """
        # 檢查是否存在該使用者且舊密碼正確
        base_query_of_check= """
        SELECT COUNT(*) FROM `user`
        WHERE u_id = %s AND password = %s
        """
        self.cursor.execute(base_query_of_check, (u_id, old_password))
        result = self.cursor.fetchone()

        if result[0] == 0:
            return "原密碼錯誤"

        # 更新密碼
        base_query_of_update = """
        UPDATE `user`
        SET password = %s 
        WHERE u_id = %s
        """
        self.cursor.execute(base_query_of_update, (new_password, u_id))
        self.connection.commit()

        return "密碼修改成功"



    def close_connection(self):
        """
        關閉資料庫連線。
        """
        try:
            if self.connection:
                self.cursor.close()
                self.connection.close()
                print("資料庫連線已關閉。")
        except pymysql.MySQLError as e:
            print(f"關閉資料庫連線失敗: {e}")

# 使用範例
if __name__ == "__main__":




    # 中華民國身分證產生器
    # https://people.debian.org/~paulliu/ROCid.html

    db = SqlAPI()
    print(db.userchangepassword(18,"securepassword","saltedpassword7777"))
    print(db.userchangepassword(10, "worng_old_pw", "saltedpassword7777"))

    #    # 用戶資訊
    #    result = db.userreg(
    #        id_num="A147909161",
    #        name="學生1",
    #        phone="0922334455",
    #        email="student@example.com",
    #        password="securepassword",
    #        address="新北市板橋區",
    #        user_type="student",
    #        s_t_id=None             # None is Null in sql
    #    )
    #
    #
    #    print(result)  # 輸出註冊結果
    #
    #    result = db.userreg(
    #        id_num="A102954995",
    #        name="評分者1",
    #        phone="0912345678",
    #        email="rater@example.com",
    #        password="securepassword",
    #        address="台北市大安區",
    #        user_type="rater",
    #        rater_title="筑波大學電腦科學系副教授"
    #    )
    #    print(result)
    #
    #    result = db.userreg(
    #        id_num="C117528249",
    #        name="教師1",
    #        phone="0933445566",
    #        email="teacher@example.com",
    #        password="securepassword",
    #        address="高雄市苓雅區",
    #        user_type="teacher",
    #        t_t_id=None  # 所屬團隊 ID
    #    )
    #    print(result)
    #    result = db.userreg(
    #        id_num="C114437590",
    #        name="超級admin",
    #        phone="0987654321",
    #        email="admin@example.com",
    #        password="securepassword",
    #        address="國立高雄大學創新學院",
    #        user_type="admin",
    #        admin_type=999
    #    )
    #    print(result)

    # 關閉資料庫連線
    db.close_connection()
