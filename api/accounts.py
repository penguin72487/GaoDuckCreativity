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
@api.route('/api/accounts/edit', methods=['GET'])
def edit_account():
    account_id = request.args.get('id', type=int)

    # 查找帳號
    account = next((acc for acc in accounts if acc.get('id') == account_id), None)

    if account:
        return jsonify({
            "message": "Account found",
            "data": account
        })
    else:
        return jsonify({
            "message": "Account not found",
            "error": True
        }), 404

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
        "name": data["name"],
        "student_id": data["student_id"],
        "email": data["email"],
        "password": data["password"],  # 注意：實際應加密密碼！
        "role": data["role"]
    }
    accounts.append(new_account)

    # 回傳成功訊息
    return jsonify({"message": "註冊成功", "data": new_account}), 201