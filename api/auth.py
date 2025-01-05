from flask import Blueprint, jsonify, request
from api.sql_connection import SqlAPI
db = SqlAPI()
auth_api = Blueprint('auth_api', __name__)

import json

# 模擬持久化存儲（可以替換為真正的數據庫）
TOKENS_FILE = "valid_tokens.json"

# 加載令牌
def load_tokens():
    try:
        with open(TOKENS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# 保存令牌
def save_tokens(tokens):
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f)

# 初始化令牌存儲
valid_tokens = load_tokens()

@auth_api.route('/login', methods=['POST'])
def login():
    data = request.json
    mail = data.get("mail")
    password = data.get("password")
    try:
        query = "SELECT * FROM user"
        db.cursor.execute(query)
        accounts = db.cursor.fetchall()
        if accounts:
            print("有數據")
        else:
            print("資料表中沒有數據")
    except Exception as e:
        print("資料庫查詢失敗:", str(e))
    if not mail or not password:
        return jsonify({"message": "學號或密碼缺失", "error": True}), 400
    columns = [
    "u_id", "ID_num", "name", "phone", "email", "password", "address",
    "is_admin", "admin_type", "is_rater", "rater_title", "is_student", "is_teacher"
    ]
    # 將 accounts 轉換為字典列表
    accounts = [dict(zip(columns, account)) for account in accounts]
    account = next(
        (acc for acc in accounts if acc.get("email") == mail and acc.get("password") == password),
        None
    )
    # 輸出結果
    if account:
        print("匹配的帳戶:", account)
        role = role_type(account)  # 角色判斷邏輯（需要實現 determine_role 函數）
        print("角色:", role)

        # 生成令牌
        token = f"token-{mail}-{role}"
        valid_tokens[token] = {"mail": mail, "role": role}
        save_tokens(valid_tokens)  # 保存令牌
        print("存儲的令牌:", valid_tokens)

        return jsonify({
            "message": "登入成功",
            "data": {"name": account["name"], "role": role, "token": token}
        }), 200

    print("找不到匹配的帳戶")
    return jsonify({"message": "學號或密碼錯誤", "error": True}), 401

def verify_token():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        print("令牌缺失或格式不正確")
        return jsonify({"message": "未提供令牌", "error": True}), 401

    token = token.split(" ")[1]  # 提取令牌
    print("驗證的令牌:", token)

    if token not in valid_tokens:
        print("令牌無效:", token)
        return jsonify({"message": "令牌無效", "error": True}), 403

    print("令牌驗證成功:", valid_tokens[token])
    return valid_tokens[token]


@auth_api.route('/protected', methods=['GET'])
def protected_route():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"message": "未提供令牌", "error": True}), 401

    token = token.split(" ")[1]
    valid_tokens.update(load_tokens())  # 每次驗證時加載最新令牌
    if token not in valid_tokens:
        return jsonify({"message": "令牌無效", "error": True}), 403

    return jsonify({"message": "授權成功", "data": valid_tokens[token]}), 200


def role_type(role):
    ro = ""
    if role.get("is_admin") == 1:
        # 如果是管理員且 admin_type 有值，返回 "管理員 + admin_type"
        if role.get("admin_type"):
            ro =  f"管理員,{role.get('admin_type')}"
        # 如果 admin_type 為 None，僅返回 "管理員"
        ro =  "管理員"
    elif role.get("is_teacher") == 1:
        ro += ",教師"
    elif role.get("is_student") == 1:
        ro += ",學生"
    elif role.get("is_rater") == 1:
        ro += ",評審"
    else:
        return "未分類角色"
    return ro