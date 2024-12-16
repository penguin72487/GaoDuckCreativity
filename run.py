import os, sys
from flask import Flask, request, jsonify
from flask_cors import CORS  # 匯入 CORS
from api import api  

app = Flask(__name__)

# 註冊所有 Blueprint
app.register_blueprint(api)
CORS(app)  # 啟用 CORS




if __name__ == '__main__':
    app.run(debug=True)
