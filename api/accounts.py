from flask import Blueprint, jsonify, request

# 定義 Blueprint
api = Blueprint('accounts_api', __name__)

# 模擬帳號資料庫
# 模擬帳號資料庫
accounts = [
    {"id": 1, "name": "王小明", "student_id": "S001", "email": "wsm@example.com", "role": "student"},
    {"id": 2, "name": "李小華", "student_id": "S002", "email": "lsh@example.com", "role": "admin"}
]

# 查詢帳號資訊
@api.route('/api/accounts', methods=['GET'])
def get_accounts():
    return jsonify({
        "accounts": accounts  # 確保返回的 key 與前端一致
    })


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


@api.route('/api/accounts/login', methods=['GET'])
def login():
    return jsonify({"message": "Login"})


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
