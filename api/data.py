from flask import Blueprint, jsonify, request

# 定義 Blueprint
api = Blueprint('data_api', __name__)

# 模擬的伺服器資料
server_data = {"message": "Initial data from /api/test endpoint"}

@api.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!1236"})
