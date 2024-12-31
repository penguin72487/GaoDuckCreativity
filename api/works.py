from flask import Blueprint, jsonify, request

# 定義 Blueprint
api = Blueprint('works_api', __name__)
works = [
        {"title": "作品一", "author": "作者甲", "description": "這是作品一的簡述"},
        {"title": "作品二", "author": "作者乙", "description": "這是作品二的簡述"},
        {"title": "作品三", "author": "作者丙", "description": "這是作品三的簡述"},
    ]
accounts = [
    {"id": 1, "name": "王小明", "student_id": "S001", "email": "wsm@example.com", "role": "student"},
    {"id": 2, "name": "李小華", "student_id": "S002", "email": "lsh@example.com", "role": "admin"}
]
@api.route('/api/works/Enroll', methods=['POST'])
def register_work():
    # 接收 JSON 數據
    data = request.json
    
    # 檢查必填欄位
    required_fields = ["competition", "name", "student_id", "department", "email", "phone"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"缺少必要欄位: {field}", "error": True}), 400

    # 模擬儲存作品資料
    new_work = {
        "competition": data["competition"],
        "name": data["name"],
        "student_id": data["student_id"],
        "department": data["department"],
        "email": data["email"],
        "phone": data["phone"],
    }

    # 在真實應用中，這裡應該插入資料庫
    # 模擬一個作品列表
    works.append(new_work)

    return jsonify({"message": "報名成功", "data": new_work}), 201



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
    
    # 返回 JSON 格式的作品資料
    return jsonify({"works": works})


@api.route('/api/works/score', methods=['GET'])
def score_work():
    return jsonify({"message": "Score work"})