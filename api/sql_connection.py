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

    def userreg(self, id_num, name, phone, email, password, address):
        """
        註冊新用戶。
        :param id_num: 身份證字號
        :param name: 中文名
        :param phone: 電話號碼
        :param email: email
        :param password: 密碼
        :param address: 住址
        :return: 註冊結果訊息

        資料庫內已對 身份證號丶email丶電話設置 unique，判斷重複註冊無需在python內處理
        本函式未對身份證號合法性做檢測
        """
        try:
            # 插入新用戶
            insert_query = """
            INSERT INTO `user` (ID_num, name, phone, email, password, address)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (id_num, name, phone, email, password, address))
            self.connection.commit()
            return "用戶註冊成功！"

        except pymysql.IntegrityError as e:
            # 捕捉 UNIQUE 約束違反的錯誤
            if "Duplicate entry" in str(e):
                if "ID_num" in str(e):
                    return "身分證字號已存在，請直接登入。"
                elif "phone" in str(e):
                    return "電話號碼已存在，請直接登入。"
                elif "email" in str(e):
                    return "電子郵件已存在，請直接登入。"
            return f"註冊失敗: {e}"

        except pymysql.MySQLError as e:
            # 處理其他 SQL 錯誤
            self.connection.rollback()
            return f"註冊失敗: {e}"

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
    db = SqlAPI()

    # 用戶資訊
    id_num = "A123456789"
    name = "王小明"
    phone = "0987654321"
    email = "test@example.com"
    password = "password123"
    address = "台北市中正區某某路123號"

    # 呼叫註冊函數
    result = db.userreg(id_num, name, phone, email, password, address)
    print(result)  # 輸出註冊結果

    # 關閉資料庫連線
    db.close_connection()
