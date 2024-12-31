from flask import Blueprint, jsonify, request
from api.accounts import accounts

# 定義 Blueprint
api = Blueprint('projects_api', __name__)
projects = [
    {
        "competition": "2025 創意競賽",
        "name": "智慧農業隊",
        "student_id": "S001",
        "competition_group": "創意發想組",
        "department": "資訊工程系",
        "email": "teamleader@example.com",
        "phone": "0912345678",
        "teacher": {
            "student_id": "S002",
            "name": "陳小華",
            "role": "teacher"
        },
        "team_members": [
            {
                "student_id": "S002",
                "name": "李小華",
                "role": "student"
            }
        ],
        "description": "path/to/description/file.pdf",
        "poster": "path/to/poster/image.png",
        "video": "https://youtube.com/demo",
        "code": "https://github.com/demo"
    }

]
@api.route('/api/projects/Enroll', methods=['POST'])
def register_project():
    # 接收 JSON 數據
    data = request.json
    
    # 檢查必填欄位
    required_fields = ["competition", "name", "student_id", "competition_group", "department", "email", "phone", "teacher"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"缺少必要欄位: {field}", "error": True}), 400

    # 檢查指導教授
    teacher = data.get("teacher")
    teacher_account = next((acc for acc in accounts if acc["student_id"] == teacher.get("student_id")), None)
    if not teacher_account or teacher_account["role"] not in ["admin", "teacher"]:
        return jsonify({"message": "指導教授無效或不存在", "error": True}), 400

    # 檢查隊員
    team_members = []
    for member in data.get("team_members", []):
        team_account = next((acc for acc in accounts if acc["student_id"] == member.get("student_id")), None)
        if not team_account:
            return jsonify({"message": f"隊員 {member.get('student_id')} 不存在", "error": True}), 400
        team_members.append(team_account)

    # 模擬文件存儲
    description_file = data.get("description")  # 模擬文件存儲
    poster_file = data.get("poster")  # 模擬文件存儲

    # 構建新項目數據
    new_project = {
        "competition": data["competition"],
        "name": data["name"],
        "student_id": data["student_id"],
        "competition_group": data["competition_group"],
        "department": data["department"],
        "email": data["email"],
        "phone": data["phone"],
        "teacher": teacher_account,
        "team_members": team_members,
        "description": description_file,  # 模擬存儲文件
        "poster": poster_file,  # 模擬存儲文件
        "video": data.get("video"),  # 選填
        "code": data.get("code")  # 選填
    }

    # 模擬保存數據（真實情況下應該插入數據庫）
    projects.append(new_project)

    return jsonify({"message": "報名成功", "data": new_project}), 201


@api.route('/api/projects/edit', methods=['GET'])
def edit_project():
    return jsonify({"message": "Edit project"})

@api.route('/api/projects/delete', methods=['GET'])
def delete_project():
    return jsonify({"message": "Delete project"})

@api.route('/api/projects/view', methods=['GET'])
def view_project():
    return jsonify({"message": "View project"})

@api.route('/api/projects/list', methods=['GET'])
def list_project():
    # 模擬作品列表資料
    
    # 返回 JSON 格式的作品資料
    return jsonify({"projects": projects})


@api.route('/api/projects/score', methods=['GET'])
def score_project():
    return jsonify({"message": "Score project"})