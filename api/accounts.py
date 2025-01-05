from flask import Blueprint, jsonify, request
# import uuid
from api.sql_connection import SqlAPI
db = SqlAPI()
# 定義 Blueprint
api = Blueprint('accounts_api', __name__)

# 模擬帳號資料庫
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
@api.route('/api/accounts', methods=['GET'])
def get_accounts():
    return jsonify({
        "accounts": accounts  # 確保返回的 key 與前端一致
    })


@api.route('/api/accounts/check', methods=['POST'])
def check_account():
    data = request.json
    ID_num = data.get("ID_num")  # 獲取前端傳來的 ID_num
    if not ID_num:
        return jsonify({"message": "缺少 ID_num 欄位", "error": True}), 400

    try:
        # 查詢資料庫，確認是否存在該 ID_num
        query = """
        SELECT ID_num, role FROM `user` WHERE ID_num = %s
        """
        db.cursor.execute(query, (ID_num,))
        result = db.cursor.fetchone()  # 獲取第一條符合的記錄
        print(result)
        if result:
            ID_num, role = result
            return jsonify({"message": "帳號存在", "data": {"ID_num": ID_num, "role": role}}), 200
        else:
            return jsonify({"message": "該學號未註冊", "error": True}), 404

    except Exception as e:
        print("檢查帳號時發生錯誤:", e)
        return jsonify({"message": "伺服器錯誤，請稍後再試", "error": True}), 500




@api.route('/api/accounts/edit', methods=['POST'])
def edit_account():
    data = request.json
    account_id = data.get("id")  # 確保前端傳遞帳號 ID

    # 找到目標帳號
    for account in accounts:
        if account["id"] == account_id:
            account.update(data)  # 更新帳號資料
            return jsonify({"message": "帳號更新成功"})

    return jsonify({"message": "帳號未找到", "error": True}), 404

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
    if data["rater_title"]=="":
        data["rater_title"]=None
    if data["stu_id"]=="":
        data["stu_id"]=None

    m = db.userreg(data["ID_num"],data["name"] , data["phone"], data["email"],data["password"], data["role"],data["rater_title"],data["stu_id"])
    print(m)
    if m == "ok":
        return jsonify({"message": "註冊成功", "data": data}), 201
    else:
        return jsonify({"message": m , "error": True}), 201
