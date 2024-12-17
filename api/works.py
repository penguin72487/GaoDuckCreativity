from flask import Blueprint, jsonify, request

# 定義 Blueprint
api = Blueprint('works_api', __name__)

@api.route('/api/works/register', methods=['GET'])
def register_work():
    return jsonify({"message": "Register work"})


@api.route('/api/works/edit', methods=['GET'])
def edit_work():
    return jsonify({"message": "Edit work"})

@api.route('/api/works/delete', methods=['GET'])
def delete_work():
    return jsonify({"message": "Delete work"})

@api.route('/api/works/view', methods=['GET'])
def view_work():
    return jsonify({"message": "View work"})

@api.route('/api/works/list', methods=['GET'])
def list_work():
    # 模擬作品列表資料
    works = [
        {"title": "作品一", "author": "作者甲", "description": "這是作品一的簡述"},
        {"title": "作品二", "author": "作者乙", "description": "這是作品二的簡述"},
        {"title": "作品三", "author": "作者丙", "description": "這是作品三的簡述"},
    ]
    # 返回 JSON 格式的作品資料
    return jsonify({"works": works})


@api.route('/api/works/score', methods=['GET'])
def score_work():
    return jsonify({"message": "Score work"})