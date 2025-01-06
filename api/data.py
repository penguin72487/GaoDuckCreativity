from flask import Blueprint, jsonify, request
from api.sql_connection import SqlAPI

# 定義 Blueprint
api = Blueprint('data_api', __name__)
db = SqlAPI()

# 模擬的伺服器資料
server_data = {"message": "Initial data from /api/test endpoint"}

@api.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "歡迎來到高雄大學激發學生創意競賽管理系統"})

# 其他 API 路由
# @api.route('/api/accounts', methods=['GET'])
# def get_accounts():
#     test_data = {
#         "accounts": [
#             { "name": "John", "student_id": "A123456789", "email": "John@gmail.com", "role": "學生" },
#             { "name": "Mary", "student_id": "B123456789", "email": "Mary@gmail,com", "role": "學生" },
#             ]
#     }
#     return jsonify(test_data)

# @api.route('/api/update_account', methods=['POST'])
# def add_account():
#     data = request.json
#     print(data)
#     return jsonify({"message": "Account added"})

# @api.route('/api/delete_account', methods=['POST'])
# def delete_account():
#     data = request.json
#     print(data)
#     return jsonify({"message": "Account deleted"})

# @api.route('/api/accounts/register', methods=['POST'])
# def accounts_register():
#     data = request.json
#     print(data)
#     return jsonify({"message": "Account registered"})