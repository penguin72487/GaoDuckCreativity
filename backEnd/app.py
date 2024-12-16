from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 解決跨域問題

# 測試 GET API
@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify({"message": "目前報名人數：30人"})

# 測試 POST API
@app.route("/api/register", methods=["POST"])
def post_data():
    data = request.json
    return jsonify({"message": f"已收到資料：{data}"})


if __name__ == "__main__":
    app.run(debug=True)
