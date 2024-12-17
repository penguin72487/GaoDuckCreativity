from flask import Blueprint, jsonify, request
# 定義 Blueprint
api = Blueprint('test_api', __name__)

# 模擬的伺服器資料
server_data = {"message": "Initial data from /api/test endpoint"}
@api.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!1236"})


@api.route('/api/test', methods=['GET'])
def get_test_data():
    # 提供前端資料
    return jsonify(server_data)

@api.route('/api/test', methods=['POST'])
def post_test_data():
    # 接收前端發送的資料
    data = request.json
    
    # 打印接收到的訊息
    print(f"Received message: {data.get('message')}")
    
    if 'message' in data:
        server_data['message'] = data['message']  # 更新伺服器資料
        return jsonify(server_data)  # 回傳更新後的資料
    else:
        return jsonify({"error": "Invalid data"}), 400



