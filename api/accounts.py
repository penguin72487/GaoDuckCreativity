from flask import Blueprint, jsonify, request

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
    student_id = data.get("student_id")

    # 確認 student_id 是否存在
    account = next((acc for acc in accounts if acc["student_id"] == student_id), None)
    if account:
        return jsonify({"message": "隊員存在", "data": account}), 200
    else:
        return jsonify({"message": "該學號未註冊", "error": True}), 404



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


# import uuid

# @api.route('/api/accounts/login', methods=['POST'])
# def login():
#     data = request.json
#     student_id = data.get("student_id")
#     password = data.get("password")

#     # 檢查必填字段
#     if not student_id or not password:
#         return jsonify({"message": "學號或密碼缺失", "error": True}), 400

#     # 驗證帳號和密碼
#     account = next((acc for acc in accounts if acc["student_id"] == student_id and acc["password"] == password), None)
#     if account:
#         # 模擬生成簡單令牌
#         token = str(uuid.uuid4())  # 使用 UUID 作為令牌
#         return jsonify({"message": "登入成功", "data": {"name": account["name"], "role": account["role"], "token": token}}), 200
#     else:
#         return jsonify({"message": "學號或密碼錯誤", "error": True}), 401



@api.route('/api/accounts/register', methods=['POST'])
def register_account():
    # 從請求中取得 JSON 資料
    data = request.json
    
    # 檢查必填欄位
    required_fields = ["name", "student_id", "email", "password", "role"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"缺少必要欄位: {field}", "error": True}), 400

    # 模擬檢查是否學號或 email 已存在
    for account in accounts:
        if account["student_id"] == data["student_id"]:
            return jsonify({"message": "學號已被註冊", "error": True}), 400
        if account["email"] == data["email"]:
            return jsonify({"message": "Email 已被註冊", "error": True}), 400

    # 新增帳號資料
    new_account = {
        "id": len(accounts) + 1,  # 自動生成 ID
        "name": data["name"],
        "student_id": data["student_id"],
        "email": data["email"],
        "password": data["password"],  # 密碼直接存儲（作業中不加密）
        "role": data["role"]
    }
    accounts.append(new_account)

    # 回傳成功訊息
    return jsonify({"message": "註冊成功", "data": new_account}), 201
