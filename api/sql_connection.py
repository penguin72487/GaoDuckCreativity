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
        驗證中華民國身分證字號是否合法
        :param id_num: 身分證字號
        :return: True 合法, False 不合法
        """
        return True #測試環境不驗證身份證合法性，正式上線時把這line去掉
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
            INSERT INTO `user` (ID_num, name, phone, email, password, address, is_admin, is_rater, is_student, is_teacher, admin_type, rater_title )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # 根據使用者類型設置對應的值
            is_admin = 1 if user_type == "admin" else 0
            is_rater = 1 if user_type == "rater" else 0
            is_student = 1 if user_type == "student" else 0
            is_teacher = 1 if user_type == "teacher" else 0

            admin_type = kwargs.get("admin_type", None)
            rater_title = kwargs.get("rater_title", None)

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
                    rater_title
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

    def isstudentinteam(self, u_id):
        """


        :param u_id: 使用者id
        :return: 隊伍id，如果uid在隊伍內。如未在隊伍，return -1
        """

        # 查詢是否為隊長的SQL語句
        check_team_leader_query = f"""
        SELECT t_id
        FROM team
        WHERE leader_u_id = {u_id}
        """

        # 查詢是否為隊員的SQL語句
        check_teammate_query = f"""
        SELECT t_id
        FROM team_student
        WHERE teammate_id = {u_id}
        """

        # 執行查詢以判斷是否為隊長
        self.cursor.execute(check_team_leader_query)
        leader_results = self.cursor.fetchall()
        self.connection.commit()
        if leader_results:
            return leader_results[0][0]  # 返回隊伍ID

        # 執行查詢以判斷是否為隊員
        self.cursor.execute(check_teammate_query)
        teammate_results = self.cursor.fetchall()
        self.connection.commit()
        if teammate_results:
            return teammate_results[0][0]  # 返回隊伍ID

        return -1  # 既不是隊長也不是隊員

    def createteam(self, t_name, leader_u_id, teacher_u_id,join_team_pass):
        """
        組織一個團隊

        t_name: 隊伍名稱varchar（20）
        leader_u_id: 隊長 uid
        teacher_u_id: 指導老師 uid
        join_team_pass: 傳入varchar（10），後續其他學生加入隊伍需要使用此password

        return :
        result[0]: 1：創建隊伍成功，-1：已存在於隊伍
        result[1]: 所屬隊伍id
        """
        result = [1,0]
        result[1]=self.isstudentinteam(4)
        if  result[1]!=-1:
            result[0]=-1
            return result

        base_query = """
                     INSERT INTO `team` (t_name, leader_u_id, teacher_u_id,join_team_pass)
                     VALUES (%s, %s, %s,%s)
                     """
        # 執行插入操作
        self.cursor.execute(
            base_query,
            (t_name, leader_u_id, teacher_u_id,join_team_pass),
        )
        # 提交變更到資料庫
        self.connection.commit()

        # 獲取自增的 t_id
        result[1] = self.cursor.lastrowid
        return result

    def jointeam(self, t_id, student_u_id, join_team_pass):
        """
        加入隊伍
        """


        #檢查是否存在在team
        team_id_result =self.isstudentinteam(student_u_id)
        if  team_id_result!=-1:
            return f"你已存在於隊伍，隊伍編號：{team_id_result}"

        #檢查授權碼是否正確
        check_join_team_pass_query = """
        SELECT t_id
        FROM team
        WHERE t_id = %s AND join_team_pass = %s
        """
        self.cursor.execute(check_join_team_pass_query, (t_id, join_team_pass))
        result = self.cursor.fetchone()
        if not result:
            return "隊伍編號或隊伍授權碼錯誤"


        #檢查隊伍是否滿人
        query = """
        SELECT COUNT(*) 
        FROM team_student
        WHERE t_id = %s
        """
        self.cursor.execute(query, (t_id))
        count = self.cursor.fetchone()[0]
        if count>4:
            return "隊伍人數已滿"


        base_query = f"""
                     INSERT INTO `team_student` ( t_id,teammate_id)
                     VALUES ({t_id}, {student_u_id})
                     """
        # 執行插入操作
        self.cursor.execute(
            base_query
        )
        # 提交變更到資料庫
        self.connection.commit()

        # 獲取自增的 t_id
        return f"成功加入隊伍，隊伍編號：{self.cursor.lastrowid}"
    def postannouncement(self,title,information,publisher_u_id):
        """
    插入公告
        """
        base_query = """
            INSERT INTO `announcement` (title, information,publisher_u_id)
            VALUES (%s, %s, %s)
             """
        self.cursor.execute(
            base_query,
            (
                title,
                information,
                publisher_u_id

            ),
        )
        self.connection.commit()
        return "發佈成功"

    def modiannouncement(self,a_id,title,information,publisher_u_id):
        """
    修改公告
    傳入： 公告id，標題，正文，發佈者id
        """
        base_query = """
UPDATE `announcement`
SET title = %s, 
    information = %s,
    publisher_u_id = %s
WHERE announcement_id = %s;
             """
        self.cursor.execute(
            base_query,
            (
                title,
                information,
                publisher_u_id,
                a_id
            ),
        )
        self.connection.commit()
        return "修改成功"





    def getannouncementlist(self,_number,_offset):
        """
    按發佈時間獲取公告
    偏移_offset筆
    一共獲取前_number筆

    return 公告id:row[0]，標題:row[1]，發佈者:row[2]
        """
        base_query=f"""
SELECT 
    announcement_id, 
    title, 
    publish_timestamp 
FROM 
    `announcement`
ORDER BY 
    publish_timestamp DESC
LIMIT {_number} OFFSET {_offset};
"""
        self.cursor.execute(base_query)
        results = self.cursor.fetchall()

        return results


    def getannouncementdetail(self,announcement_id):
        """
    按獲取公告id=announcement_id的公告

    return：
    row[0]:公告標題
    row[1]:發佈者u_id
    row[2]:內文
    row[3]:發佈時間
    row[4]:最後修改時間

        """
        base_query = f"""
        SELECT title,publisher_u_id, information, publish_timestamp,last_update_timestamp
        FROM `announcement`
        where announcement_id = {announcement_id};
             """
        self.cursor.execute(base_query)
        result = self.cursor.fetchone()

        return result





    def submitproject(self, p_name,description, poster_file_id, video_link, github_link, t_id):


        #檢查該隊伍是否已有project
        check_project_query="""
        select p_id
        from `project`
        where t_id = %s"""
        self.cursor.execute(check_project_query, (t_id))
        # 如果該隊伍已有專案，則返回error
        if self.cursor.fetchone():
            return f"該隊伍已經有project"





        base_query = f"""
                    INSERT INTO `project` (p_name, `description`, `poster_file_id`, `video_link`, `github_link`, `t_id`) 
                    VALUES ( %s,%s, %s, %s, %s, %s)
                  """
        self.cursor.execute(base_query, (p_name,description, poster_file_id, video_link, github_link, t_id))
        self.connection.commit()
        return "succ"

    def getprojectlist(self, _number, _offset):
        base_query = f"""
          SELECT 
              p_name, 
              description
               
          FROM 
              `project`
          ORDER BY 
              time DESC
          LIMIT {_number} OFFSET {_offset};
          """
        self.cursor.execute(base_query)
        results = self.cursor.fetchall()
        return results
    def getprojectdetail(self,t_id):
        base_query = f"""
        SELECT *
        FROM `project`
        where t_id = {t_id};
             """
        self.cursor.execute(base_query)
        result = self.cursor.fetchone()

        return result
    def modiproject(self, p_name,description, poster_file_id, video_link, github_link, t_id):
        _p_id=self.getproject(t_id)
        if _p_id==None:
            return "你的隊伍沒有提交過project"


        base_query = """
        UPDATE `project`
        SET p_name = %s,
            description = %s,
            poster_file_id = %s,
            video_link = %s,
            github_link = %s
        WHERE p_id = %s;
                     """
        self.cursor.execute(
            base_query,
            (
             p_name,description,poster_file_id,video_link,github_link,_p_id[0]
            ),
        )
        self.connection.commit()
        return "修改成功"

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
    #print(db.userchangepassword(18,"securepassword","saltedpassword7777"))
    #print(db.userchangepassword(10, "worng_old_pw", "saltedpassword7777"))







###############################
#########announcement
    #db.postannouncement("標afa題","<br>aaa2<br>","18")
    #results_of_getann_list=db.getannouncementlist("2",3)
    #for row in results_of_getann:
    #print(f"ID: {row[0]}, Title: {row[1]}, Publish Time: {row[2]}")
    #results_of_getann_body=db.getannouncementdetail("2"
    #print(f"title: {results_of_getann_body[0]}, pubish_u_id: {results_of_getann_body[1]},body: {results_of_getann_body[2]} .Publish Time: {results_of_getann_body[3]} last Update Time: {results_of_getann_body[4]}")
    #db.modiannouncement(1,"測試修改標題","<br><h1>測試正文</h1><p>abc</p>","18")





#########################
########project:
    #print(db.submitproject("test","非常有創意的project","3","https://youtube.com/xxx","https://github.com/xxx","5"))
    #print(db.getprojectdetail(5))
    #print(db.modiproject("cesi", "非常SB的project", "3", "https://youtube.com/yyy", "https://github.com/yyy", "5"))



######################################################
############team:
    #print(db.createteam("屌爆了","4","10","AWVISAJWNS"))
    #print(db.jointeam("5","7","AWVISAJW2NS"))

    #print(db.isstudentinteam(4))
    #print(db.jointeam(5,24,"AWVISAJWNS"))
    #print(db.jointeam(5,25,"AWVISAJWNS"))
    #print(db.jointeam(5,26,"AWVISAJWNS"))
    #print(db.jointeam(5,27,"AWVISAJWNS2")) #pw worng
    #print(db.jointeam(5,28,"AWVISAJWNS"))
    #print(db.jointeam(5,29,"AWVISAJWNS"))
    #print(db.jointeam(5,31,"AWVISAJWNS"))
    #print(db.jointeam(5,30,"AWVISAJWNS2")) #pw worng

















    #    # 用戶資訊
    #    result = db.userreg(
    #        id_num="A147909161",
    #        name="學生1",
    #        phone="0922334455",
    #        email="student@example.com",
    #        password="securepassword",
    #        address="新北市板橋區",
    #        user_type="student",
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
