from flask import Blueprint, jsonify, request
from api.sql_connection import SqlAPI
db = SqlAPI()
# 定義 Blueprint
api = Blueprint('accounts_api', __name__)

# 模擬帳號資料庫
accounts = [
    {"id": 1, "name": "王小明", "student_id": "S001", "email": "wsm@example.com", "password": "123456", "role": "student"},
    {"id": 2, "name": "李小華", "student_id": "S002", "email": "lsh@example.com", "password": "123456", "role": "admin"},
    {"id": 3, "name": "張大強", "student_id": "S003", "email": "zdq@example.com", "password": "123456", "role": "student"},
    {"id": 4, "name": "林小真", "student_id": "S004", "email": "lxz@example.com", "password": "123456", "role": "student"},
    {"id": 5, "name": "陳冠希", "student_id": "S005", "email": "cgx@example.com", "password": "123456", "role": "student"},
    {"id": 6, "name": "黃美麗", "student_id": "S006", "email": "hml@example.com", "password": "123456", "role": "student"},
    {"id": 7, "name": "楊志偉", "student_id": "S007", "email": "yzw@example.com", "password": "123456", "role": "rater"},
    {"id": 8, "name": "李佳瑩", "student_id": "S008", "email": "ljy@example.com", "password": "123456", "role": "student"},
    {"id": 9, "name": "鄭凱文", "student_id": "S009", "email": "zkw@example.com", "password": "123456", "role": "student"},
    {"id": 10, "name": "趙曉東", "student_id": "S010", "email": "zxd@example.com", "password": "123456", "role": "student"},
    {"id": 11, "name": "劉婷婷", "student_id": "S011", "email": "ltt@example.com", "password": "123456", "role": "admin"},
    {"id": 12, "name": "吳建國", "student_id": "S012", "email": "wjg@example.com", "password": "123456", "role": "student"},
    {"id": 13, "name": "郭麗華", "student_id": "S013", "email": "glh@example.com", "password": "123456", "role": "student"},
    {"id": 14, "name": "許志明", "student_id": "S014", "email": "xzm@example.com", "password": "123456", "role": "rater"},
    {"id": 15, "name": "周雲龍", "student_id": "S015", "email": "zyl@example.com", "password": "123456", "role": "student"},
    {"id": 16, "name": "葉小英", "student_id": "S016", "email": "yxy@example.com", "password": "123456", "role": "teacher"},
    {"id": 17, "name": "鄧曉明", "student_id": "S017", "email": "dxm@example.com", "password": "123456", "role": "teacher"},
    {"id": 18, "name": "方志強", "student_id": "S018", "email": "fzq@example.com", "password": "123456", "role": "teacher"},
    {"id": 19, "name": "韓秀芳", "student_id": "S019", "email": "hxf@example.com", "password": "123456", "role": "teacher"},
    {"id": 20, "name": "謝忠誠", "student_id": "S020", "email": "xzc@example.com", "password": "123456", "role": "admin"},
]

# 查詢帳號資訊
@api.route('/api/accounts/get', methods=['GET'])
def get_accounts():
    print("get_accounts")
    try:
        print("get_accounts query")
        query = "SELECT * FROM user"
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        result = [{"ID_num": r[1], "name": r[2], "email": r[4], "rater_title": r[6], "role": r[7], "stu_id": r[8]} for r in result]
        return jsonify({"accounts": result})  # 包裹在 accounts 对象中
    except Exception as e:
        print("Database error:", e)
        return jsonify({"error": "Database connection failed"}), 500



@api.route('/api/accounts/check', methods=['POST'])
def check_account():
    data = request.json
    u_id = data.get("u_id")  # 獲取前端傳來的 u_id
    if not u_id:
        return jsonify({"message": "缺少 u_id 欄位", "error": True}), 400

    try:
        # 查詢資料庫，確認是否存在該 u_id
        query = """
        SELECT u_id, role FROM `user` WHERE u_id = %s
        """
        db.cursor.execute(query, (u_id,))
        result = db.cursor.fetchone()  # 獲取第一條符合的記錄
        print(result)
        if result:
            u_id, role = result
            return jsonify({"message": "帳號存在", "data": {"u_id": u_id, "role": role}}), 200
        else:
            return jsonify({"message": "該帳號未註冊", "error": True}), 404

    except Exception as e:
        print("檢查帳號時發生錯誤:", e)
        return jsonify({"message": "伺服器錯誤，請稍後再試", "error": True}), 500

@api.route('/api/accounts/edit', methods=['POST'])
def edit_account():
    print("edit_account")
    data = request.json
    print("Received data:", data)

    # 获取前端传递的数据
    ID_num = data.get("ID_num")
    name = data.get("name")
    email = data.get("email")
    role = data.get("role")
    if role == "student":
        role = "1"
    elif role == "teacher":
        role = "2"
    elif role == "rater":
        role = "3"
    elif role == "admin":
        role = "99"
    rater_title = data.get("rater_title") or None  # 空字符串处理为 None
    stu_id = data.get("stu_id") or None  # 空字符串处理为 None

    if not ID_num:
        return jsonify({"message": "缺少 ID_num 欄位", "error": True}), 400

    try:
        # 参数化查询，更新用户信息
        query = """
            UPDATE user 
            SET name = %s, email = %s, role = %s, rater_title = %s, stu_id = %s 
            WHERE ID_num = %s
        """
        db.cursor.execute(query, (name, email, role, rater_title, stu_id, ID_num))

        if db.cursor.rowcount > 0:  # 检查是否更新成功
            print("帳號更新成功")
            return jsonify({"message": "帳號更新成功"}), 200
        else:
            print("未找到指定帳號")
            return jsonify({"message": "未找到指定帳號", "error": True}), 404

    except Exception as e:
        print("編輯帳號時發生錯誤:", e)
        return jsonify({"message": "伺服器錯誤，請稍後再試", "error": True}), 500



@api.route('/api/accounts/delete', methods=['POST'])
def delete_account():
    data = request.json
    account_id = data.get("id")

    global accounts
    accounts = [acc for acc in accounts if acc["id"] != account_id]  # 過濾掉目標帳號

    return jsonify({"message": "帳號刪除成功"})

@api.route('/api/accounts/register', methods=['POST'])
def register_account():
    # 從請求中取得 JSON 資料
    data = request.json
    print(data)
    if data["rater_title"] == "":
        data["rater_title"] = None
    if data["stu_id"] == "":
        data["stu_id"] = None

    m = db.userreg(data["ID_num"], data["name"], data["phone"], data["email"], data["password"], data["role"], data["rater_title"], data["stu_id"])
    print(m)
    if m == "ok":
        return jsonify({"message": "註冊成功", "data": data}), 201
    else:
        return jsonify({"message": m, "error": True}), 201