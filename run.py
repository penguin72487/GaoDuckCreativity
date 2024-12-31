import os, sys
from flask import Flask, request, jsonify
from flask_cors import CORS  # 匯入 CORS
from api import api  
from api.auth import auth_api

from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# 註冊所有 Blueprint
app.register_blueprint(api)
app.register_blueprint(auth_api, url_prefix='/api/auth')
CORS(app)  # 啟用 CORS

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    return jsonify({"error": "伺服器發生未預期的錯誤"}), 500



if __name__ == '__main__':
    app.run(debug=True)
