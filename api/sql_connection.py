import pymysql
import json
import os
class SqlAPI:
    def __init__(self ):
        """
        讀取 sql_config.json 內參數進行連接

        """
        try:
            with open(os.path.join(os.path.dirname(__file__), "config/sql_config.json"), 'r') as file:
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


            print(f"檔案無法讀取: {e}")

        except (pymysql.MySQLError, FileNotFoundError, KeyError) as e:

            print(f"資料庫連線失敗或配置檔案錯誤: {e}")
    def getusertype(self,u_id):
        base_query = "select role from user where u_id=%s"
        self.cursor.execute(base_query, (u_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None


    def userreg(self,ID_num, name, phone, email, password, role, rater_title,stu_id):
        """
        註冊新用戶。
        :param ID_num: username
        :param name: 中文名
        :param phone: 電話號碼
        :param email: email
        :param password: 密碼
        :param role: 使用者類型 ('admin', 'rater', 'student', 'teacher') 1=學生，2=老師，3=評委，99=admin
        :param stu_id: 學號（僅學生需要輸入）
        :return: 註冊結果訊息
        資料庫內已對 身份證號丶email丶電話設置 unique，判斷重複註冊無需在python內處理

        """
        try:
            role_code=0
            if role=="student":
                role_code=1
            elif role=="teacher":
                role_code=2
            elif role=="rater":
                role_code=3
            elif role=="admin":
                role_code=99
            # 基本插入查詢
            base_query = """
            INSERT INTO `user` (ID_num, name, phone, email, password, role, rater_title,stu_id )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            # 執行插入
            self.cursor.execute(
                base_query,
                (ID_num, name, phone, email, password, role_code, rater_title,stu_id
                ),
            )
            self.connection.commit()
            return "ok"

        except pymysql.IntegrityError as e:
            # 處理唯一性約束錯誤
            if "Duplicate entry" in str(e):
                if "ID_num" in str(e):
                    return "使用者名稱已存在，請確認或使用其他使用者名稱。"
                elif "phone" in str(e):
                    return "電話號碼已存在，請確認或使用其他電話號碼。"
                elif "email" in str(e):
                    return "電子郵件已存在，請確認或使用其他電子郵件。"
                elif "stu_id" in str(e):
                    return "學號已存在，請確認或使用其他學號。"
            return f"註冊失敗: {e}"

        except pymysql.MySQLError as e:
            # 處理其他 SQL 錯誤
            self.connection.rollback()
            return f"註冊失敗: {e}"



    def userlogin(self,account,password):
        """
        登入
        :param account: ID_num/email/phone
        :param password: password
        :return: succ:u_id; fail:-1
        """
        base_query = """select u_id from user 
        where (phone=%s or ID_num=%s or email=%s )and password=%s
        """
        self.cursor.execute(base_query, (account, account, account, password))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return -1



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
        result[1]=self.isstudentinteam(leader_u_id)
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
        return 'succ'
        #return f"成功加入隊伍，隊伍編號：{self.cursor.lastrowid}"

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

    def deleteannouncement(self,a_id):
        base_query="""
        DELETE FROM `announcement`
        where announcement_id = %s;"""
        self.cursor.execute(base_query, (a_id,))
        self.connection.commit()
        return "succ"


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





    def submitproject(self,leader_id,teammate2_id,teammate3_id,teammate4_id,teammate5_id,teammate6_id,teacher_id,p_name,description_file,poster_file,video_link,github_link):
        """


        :param leader_id:
        :param teammate2_id:
        :param teammate3_id:非必填
        :param teammate4_id:非必填
        :param teammate5_id:非必填
        :param teammate6_id:非必填
        :param teacher_id:
        :param p_name:
        :param description_file:
        :param poster_file:
        :param video_link:
        :param github_link:
        :return:
        """
        #檢查該學生是否已有project
        student_ids = [leader_id,teammate2_id,teammate3_id,teammate4_id,teammate5_id,teammate6_id]
        student_ids = [stuno for stuno in student_ids if stuno is not None]

        check_project_query=f"""
        select p_id
        from `project`
            WHERE leader_id IN ({', '.join(map(str, student_ids))})
       OR teammate2_id IN ({', '.join(map(str, student_ids))})
       OR teammate3_id IN ({', '.join(map(str, student_ids))})
       OR teammate4_id IN ({', '.join(map(str, student_ids))})
       OR teammate5_id IN ({', '.join(map(str, student_ids))})
       OR teammate6_id IN ({', '.join(map(str, student_ids))});
        """
        self.cursor.execute(check_project_query)
        # 如果該隊伍已有專案，則返回error
        if self.cursor.fetchone():
            return f"其中一位/隊長隊員已上傳project"





        base_query = f"""
                    INSERT INTO `project` ( leader_id,teammate2_id,teammate3_id,teammate4_id,teammate5_id,teammate6_id,teacher_id,p_name,description_file,poster_file,video_link,github_link)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                  """
        self.cursor.execute(base_query, (leader_id,teammate2_id,teammate3_id,teammate4_id,teammate5_id,teammate6_id,teacher_id,p_name,description_file,poster_file,video_link,github_link))
        self.connection.commit()
        return "succ"

    def getprojectlist(self, _number, _offset):
        base_query = f"""
          SELECT 
              p_name, p_id
              
               
          FROM 
              `project`
          ORDER BY 
              time DESC
          LIMIT {_number} OFFSET {_offset};
          """
        self.cursor.execute(base_query)
        results = self.cursor.fetchall()
        return results
    def getprojectdetail(self,p_id):
        base_query = f"""
        SELECT *
        FROM `project`
        where p_id = {p_id};
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

    def uploadfile(self,path,uploader_t_id):
        """
        檔案保存到伺服器後，保存檔案的路徑

        :param path: 檔案保存的路徑
        :param uploader_t_id: 學生上傳：隊伍id，管理員上傳：None
        :return:檔案id file_id
        """

        base_query = """
                  INSERT INTO `file` ( file_path, uploader_t_id)
                  VALUES (%s, %s)
                   """
        self.cursor.execute(
            base_query,
            (
               path,
                uploader_t_id

            ),
        )
        self.connection.commit()
        return self.cursor.lastrowid
    def getfile(self,file_id):
        self.getfile(file_id,None)
    def getfile(self,file_id,viewer):
        """
        獲取檔案在伺服器上的路徑
        :param file_id:
        :param viewer:已登入情況下：使用者u_id；未登入情況下：None
        :return:檔案路徑 / 403非法存取
        """


        base_query="""
        select * from `file`
        where file_id = %s
        """
        self.cursor.execute(base_query,(file_id))
        result = self.cursor.fetchone()
        #如果是管理員上傳的檔案，任何人都能存取
        if result[2] ==None:
            return result[1]
        if viewer == None:
            return "403"
        #如果非管理員上傳，只能由上傳者所屬隊伍的學生和老師丶評審委員丶管理員讀取
        check_if_admin_or_rater_or_admin = """
        select u_id
        from   `user`
        where (u_id = %s) and(is_admin = 1 or is_rater = 1)"""

        self.cursor.execute(check_if_admin_or_rater_or_admin,(viewer))
        result_of_check_if_admin_or_rater_or_admin = self.cursor.fetchone()
        #print(result_of_check_if_admin_or_rater_or_admin)
        if not result_of_check_if_admin_or_rater_or_admin == None: #是管理員/評審委員
            return result[1]

        #不是管理員/評審委員，判斷是否是檔案上傳隊伍的所屬學生/老師
        check_if_teacher_or_teammate_in_team="""
                                    select t_id from `team`
                                    where leader_u_id=%s or teacher_u_id=%s
                                    union
                                    select t_id from `team_student`
                                    where teammate_id=%s"""
        self.cursor.execute(check_if_teacher_or_teammate_in_team,(viewer,viewer,viewer))
        result_of_check_if_teacher_or_teammate_in_team = self.cursor.fetchone()

        if not result_of_check_if_teacher_or_teammate_in_team == None: #檔案上傳隊伍的所屬學生/老師
            return result[1]

        return "403"
    def rateproject(self,rater_u_id,p_id,s_creativity,s_usability,s_design,s_completeness):
        """

        :param rater_u_id:  評審委員u_id
        :param p_id:    project id
        :param s_creativity:  創意性評分 int 1~10
        :param s_usability:  可用性評分 int 1~10
        :param s_design:    設計評分 int 1~10
        :param s_completeness:   完成度評分 int 1~10
        :return: 成功or失敗
        """
        #檢查是否已經評價過
        check_rate_history="""
        select water_id from `review`
        where p_id=%s and rater_u_id=%s"""
        self.cursor.execute(check_rate_history,(p_id,rater_u_id))
        result_of_check_rate_history = self.cursor.fetchone()
        if not  result_of_check_rate_history == None:
            return "failed 該評委已對該作品進行評價"



        base_query="""
        insert into `review`(rater_u_id,p_id,s_creativity,s_usability,s_design,s_completeness)
            values (%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(base_query,(rater_u_id,p_id,s_creativity,s_usability,s_design,s_completeness))
        self.connection.commit()
        return "success"
    def getrate(self,p_id,rater_u_id):
        """


        :param p_id:
        :param rater_u_id:
        :return:
        """
        base_query="""
        select * from `review`
        where p_id = %s and rater_u_id = %s"""
        self.cursor.execute(base_query,(p_id,rater_u_id))
        result = self.cursor.fetchone()
        return result

    def modirate(self,rater_u_id,p_id,s_creativity,s_usability,s_design,s_completeness):
        """
        評委修改評分

        :param rater_u_id:  評審委員u_id
        :param p_id:    project id
        :param s_creativity:  創意性評分 int 1~10
        :param s_usability:  可用性評分 int 1~10
        :param s_design:    設計評分 int 1~10
        :param s_completeness:   完成度評分 int 1~10
        :return:成功
        """
        base_query="""
        update `review`
        set s_creativity = %s,
        s_usability = %s,
        s_design = %s,
        s_completeness = %s
        where p_id = %s and rater_u_id = %s
        """
        self.cursor.execute(base_query,(s_creativity,s_usability,s_design,s_completeness,p_id,rater_u_id))
        self.connection.commit()
        return "success"


    def getavgrate(self,p_id):
        """
        獲取project平均分
        :param p_id: project id
        :return: 該project的四項得分的評委平均分
        """
        base_query ="""
                            SELECT 
                        p_id, 
                        AVG(s_creativity) AS avg_creativity,
                        AVG(s_usability) AS avg_usability,
                        AVG(s_design) AS avg_design,
                        AVG(s_completeness) AS avg_completeness
                    FROM review
                    where p_id = %s
                    GROUP BY p_id;
                            """
        self.cursor.execute(base_query,(p_id))
        result = self.cursor.fetchone()
        return result


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
#

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




#############################
########file:
    #print(db.uploadfile("apic_awubd.webp",None))
    #print(db.uploadfile("apic_awubd.webp","5"))

    #print(db.getfile(6,7)) #評審
    #print(db.getfile(6,18)) #admin
    #print(db.getfile(6,4)) #學生：隊長
    #print(db.getfile(6,28)) #學生：隊員
    #print(db.getfile(6,38)) #學生：非該隊學生
    #print(db.getfile(6,39)) #老師：非指導老師
    #print(db.getfile(6,10)) #老師：指導老師





##############################################
########評分：
    #print(db.rateproject(p_id=1,rater_u_id=40,s_creativity=4,s_usability=5,s_design=6,s_completeness=8))
    ##print(db.rateproject(p_id=1,rater_u_id=41,s_creativity=4,s_usability=5,s_design=7,s_completeness=9))
    #print(db.getrate(rater_u_id=40,p_id=1))
    #print(db.modirate(p_id=1,rater_u_id=40,s_creativity=9,s_usability=8,s_design=7,s_completeness=6))
    #print(db.getrate(rater_u_id=40,p_id=1))

    #print(db.getusertype(4))
    #print(db.getusertype(7))
    #print(db.getusertype(10))
    #print(db.getusertype(18))
    #print(db.getavgrate(1))

    #result = db.userreg(
    #    ID_num="Q144909361",
    #    name="學生2",
    #    phone="0922344450",
    #    email="studen222t@example.com",
    #    password="securepassword",
    #    role="student",
    #    rater_title=None,
    #    stu_id="A1154444"
    #)
    #result = db.userreg(
    #    ID_num="banana2",
    #    name="評委Banana2",
    #    phone="0955882277",
    #    email="bananana222na@example.com",
    #    password="securepassword",
    #    role="rater",
    #    rater_title="交大校長",
    #    stu_id=None
    #)

    result=db.submitproject(p_id=1)
    print(result)  # 輸出註冊結果
    #
    #result = db.userreg(
    #        id_num="A102954775",
    #        name="評分者2",
    #        phone="0966444555",
    #        email="rater2@example.com",
    #        password="securepassword",
    #        address="福建省連江縣",
    #        user_type="rater",
    #        rater_title="金門大學電機工程學系教授"
    #    )
    #result = db.userreg(
    #        id_num="K52156#6325",
    #        name="評分者3",
    #        phone="0966777555",
    #        email="rater3@example.co.kr",
    #        password="securepassword",
    #        address="korea",
    #        user_type="rater",
    #        rater_title="韓國科學技術院信息和通訊工程系講座教授"
    #    )
    #print(result)
    #
    #result = db.userreg(
    #    id_num="Z117528222",
    #    name="教師2",
    #    phone="0922222222",
    #    email="two@222.com",
    #    password="securepassword",
    #    address="高雄市三民區",
    #    user_type="teacher",
    #)
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
