from flask import Blueprint, jsonify, request

# 定義 Blueprint
api = Blueprint('data_api', __name__)

# 模擬的伺服器資料
server_data = {"message": "Initial data from /api/test endpoint"}

@api.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!1236"})

# 模擬公告資料
announcements = [
    {
        "title": "系統維護公告",
        "date": "2025-01-05",
        "content": "系統將於 2025 年 1 月 10 日進行維護，期間可能無法正常使用。",
        "link": "https://example.com/maintenance"
    },
    {
        "title": "活動通知",
        "date": "2025-01-01",
        "content": "我們將於 2025 年 1 月 15 日舉行線上分享會，歡迎參加！",
        "link": "https://example.com/event"
    },
    {
        "title": "新功能上線",
        "date": "2024-12-25",
        "content": "新版功能已上線，請登入系統查看詳細資訊。",
        "link": None
    }
]

# 公告 API
@api.route('/api/announcements', methods=['GET'])
def get_announcements():
    
    return jsonify({"announcements": announcements})

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