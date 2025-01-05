import os, sys
from flask import Flask, request, jsonify
from flask_cors import CORS  # 匯入 CORS
from api.data import api as data_api
from api.auth import auth_api
from api.announcement_control import announcement_api

from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# 註冊所有 Blueprint
app.register_blueprint(data_api)
app.register_blueprint(auth_api, url_prefix='/api/auth')
app.register_blueprint(announcement_api)
CORS(app)  # 啟用 CORS

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    return jsonify({"error": "伺服器發生未預期的錯誤"}), 500

if __name__ == '__main__':
    app.run(debug=True)