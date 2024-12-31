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