from flask import Blueprint, jsonify, request
from api.accounts import accounts

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
    student_id = data.get("student_id")
    password = data.get("password")

    if not student_id or not password:
        return jsonify({"message": "學號或密碼缺失", "error": True}), 400

    account = next((acc for acc in accounts if acc["student_id"] == student_id and acc["password"] == password), None)
    if account:
        token = f"token-{student_id}-{account['role']}"
        valid_tokens[token] = {"student_id": student_id, "role": account["role"]}
        save_tokens(valid_tokens)  # 保存令牌
        print("存儲的令牌:", valid_tokens)
        return jsonify({"message": "登入成功", "data": {"name": account["name"], "role": account["role"], "token": token}}), 200

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