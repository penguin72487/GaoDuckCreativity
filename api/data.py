from flask import Blueprint, jsonify, request

# 定義 Blueprint
api = Blueprint('data_api', __name__)

# 模擬的伺服器資料
server_data = {"message": "Initial data from /api/test endpoint"}

@api.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!1236"})

@api.route('/api/announcements', methods=['GET'])
def get_announcement():
    test_data = {
        "announcements": [
            { "date": "2024/12/10", "title": "比賽報名截止延長至12/31", "link": "#" },
            { "date": "2024/12/05", "title": "新增作品上傳格式說明", "link": "#" },
            { "date": "2024/12/01", "title": "評審名單公布", "link": "#" },
            { "date": "2024/12/01", "title": "比賽報名開始", "link": "#" }
        ]
    }

    return jsonify(test_data)

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
# #     return jsonify({"message": "Account added", "data": data})

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