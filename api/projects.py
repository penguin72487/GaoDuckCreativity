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
        "teacher": {
            "student_id": "T001",
            "name": "陳小華",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S002", "name": "李小華", "role": "student"},
            {"student_id": "S003", "name": "王大明", "role": "student"}
        ],
        "description": "path/to/description/file1.pdf",
        "poster": "path/to/poster/image1.png",
        "video": "https://youtube.com/demo1",
        "code": "https://github.com/demo1"
    },
    {
        "competition": "2025 創意競賽",
        "name": "智慧醫療隊",
        "student_id": "S004",
        "competition_group": "創業實作組",
        "teacher": {
            "student_id": "T002",
            "name": "黃美英",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S005", "name": "張小華", "role": "student"},
            {"student_id": "S006", "name": "林志強", "role": "student"}
        ],
        "description": "path/to/description/file2.pdf",
        "poster": "path/to/poster/image2.png",
        "video": "https://youtube.com/demo2",
        "code": "https://github.com/demo2"
    },
    {
        "competition": "2025 創意競賽",
        "name": "智慧家居隊",
        "student_id": "S007",
        "competition_group": "創意發想組",
        "teacher": {
            "student_id": "T003",
            "name": "林冠華",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S008", "name": "周小龍", "role": "student"},
            {"student_id": "S009", "name": "鄭美麗", "role": "student"}
        ],
        "description": "path/to/description/file3.pdf",
        "poster": "path/to/poster/image3.png",
        "video": "https://youtube.com/demo3",
        "code": None
    },
    {
        "competition": "2025 創意競賽",
        "name": "智慧校園隊",
        "student_id": "S010",
        "competition_group": "創業實作組",
        "teacher": {
            "student_id": "T004",
            "name": "李建國",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S011", "name": "何小芬", "role": "student"}
        ],
        "description": None,
        "poster": "path/to/poster/image4.png",
        "video": None,
        "code": "https://github.com/demo4"
    },
    {
        "competition": "2025 創意競賽",
        "name": "環保創新隊",
        "student_id": "S012",
        "competition_group": "創意發想組",
        "teacher": {
            "student_id": "T005",
            "name": "許志明",
            "role": "teacher"
        },
        "team_members": [],
        "description": "path/to/description/file5.pdf",
        "poster": None,
        "video": "https://youtube.com/demo5",
        "code": "https://github.com/demo5"
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