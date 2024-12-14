from flask import Flask, request, jsonify
from flask_cors import CORS  # 匯入 CORS

app = Flask(__name__)
CORS(app)  # 啟用 CORS

# 模擬的伺服器資料
server_data = {"message": "Initial data from /api/test endpoint"}

@app.route('/api/test', methods=['GET'])
def get_test_data():
    # 提供前端資料
    return jsonify(server_data)

@app.route('/api/test', methods=['POST'])
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

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(debug=True)
