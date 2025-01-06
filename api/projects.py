from flask import Blueprint, jsonify, request
from api.accounts import accounts
from api.sql_connection import SqlAPI
db = SqlAPI()
# 定義 Blueprint
api = Blueprint('projects_api', __name__)
projects= [
    # 2025 年專案
    {
        "tid" : 1,
        "competition": "2025 創意競賽",
        "name": "智能交通管理隊",
        "student_id": "S013",
        "competition_group": "創業實作組",
        "teacher": {
            "student_id": "T006",
            "name": "高俊傑",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S014", "name": "林志玲", "role": "student"},
            {"student_id": "S015", "name": "陳曉東", "role": "student"}
        ],
        "description": "path/to/description/file6.pdf",
        "poster": "path/to/poster/image6.png",
        "video": "https://youtube.com/demo6",
        "code": "https://github.com/demo6"
    },
    {
        "tid" : 2,
        "competition": "2025 創意競賽",
        "name": "智能農業應用隊",
        "student_id": "S016",
        "competition_group": "創意發想組",
        "teacher": {
            "student_id": "T007",
            "name": "陳志明",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S017", "name": "李志豪", "role": "student"},
            {"student_id": "S018", "name": "王小美", "role": "student"}
        ],
        "description": None,
        "poster": None,
        "video": "https://youtube.com/demo7",
        "code": None
    },
    {
        "tid" : 3,
        "competition": "2025 創意競賽",
        "name": "健康管理隊",
        "student_id": "S019",
        "competition_group": "創業實作組",
        "teacher": {
            "student_id": "T008",
            "name": "黃淑芬",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S020", "name": "張志文", "role": "student"}
        ],
        "description": "path/to/description/file7.pdf",
        "poster": "path/to/poster/image7.png",
        "video": None,
        "code": "https://github.com/demo7"
    },
    {
        "tid" : 4,
        "competition": "2025 創意競賽",
        "name": "環保能源管理隊",
        "student_id": "S021",
        "competition_group": "創意發想組",
        "teacher": {
            "student_id": "T009",
            "name": "楊志強",
            "role": "teacher"
        },
        "team_members": [],
        "description": None,
        "poster": None,
        "video": "https://youtube.com/demo8",
        "code": None
    },

    # 2024 年專案
    {
        "tid" : 5,
        "competition": "2024 創意競賽",
        "name": "智能物流隊",
        "student_id": "S022",
        "competition_group": "創業實作組",
        "teacher": {
            "student_id": "T010",
            "name": "吳小明",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S023", "name": "張小華", "role": "student"},
            {"student_id": "S024", "name": "李大華", "role": "student"}
        ],
        "description": "path/to/description/file8.pdf",
        "poster": None,
        "video": None,
        "code": "https://github.com/demo8"
    },
    {
        "tid" : 6,
        "competition": "2024 創意競賽",
        "name": "醫療大數據隊",
        "student_id": "S025",
        "competition_group": "創意發想組",
        "teacher": {
            "student_id": "T011",
            "name": "陳小華",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S026", "name": "黃志勇", "role": "student"}
        ],
        "description": "path/to/description/file9.pdf",
        "poster": "path/to/poster/image9.png",
        "video": "https://youtube.com/demo9",
        "code": None
    },
    {
        "tid" : 7,
        "competition": "2024 創意競賽",
        "name": "自動化生產隊",
        "student_id": "S027",
        "competition_group": "創業實作組",
        "teacher": {
            "student_id": "T012",
            "name": "李建華",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S028", "name": "何美麗", "role": "student"}
        ],
        "description": None,
        "poster": "path/to/poster/image10.png",
        "video": "https://youtube.com/demo10",
        "code": "https://github.com/demo10"
    },
    {
        "tid" : 8,
        "competition": "2024 創意競賽",
        "name": "智能社區管理隊",
        "student_id": "S029",
        "competition_group": "創意發想組",
        "teacher": {
            "student_id": "T013",
            "name": "高志明",
            "role": "teacher"
        },
        "team_members": [],
        "description": None,
        "poster": None,
        "video": None,
        "code": None
    },

    # 2023 年專案
    {
        "tid" : 9,
        "competition": "2023 創意競賽",
        "name": "農業機械化隊",
        "student_id": "S030",
        "competition_group": "創業實作組",
        "teacher": {
            "student_id": "T014",
            "name": "陳志華",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S031", "name": "吳志強", "role": "student"}
        ],
        "description": "path/to/description/file11.pdf",
        "poster": "path/to/poster/image11.png",
        "video": None,
        "code": None
    },
    {
        "tid" : 10,
        "competition": "2023 創意競賽",
        "name": "智慧城市隊",
        "student_id": "S032",
        "competition_group": "創意發想組",
        "teacher": {
            "student_id": "T015",
            "name": "黃美華",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S033", "name": "張志偉", "role": "student"},
            {"student_id": "S034", "name": "林建國", "role": "student"}
        ],
        "description": None,
        "poster": "path/to/poster/image12.png",
        "video": "https://youtube.com/demo11",
        "code": "https://github.com/demo11"
    },
    {
        "tid" : 11,
        "competition": "2023 創意競賽",
        "name": "智能家電隊",
        "student_id": "S035",
        "competition_group": "創業實作組",
        "teacher": {
            "student_id": "T016",
            "name": "李志偉",
            "role": "teacher"
        },
        "team_members": [],
        "description": None,
        "poster": None,
        "video": "https://youtube.com/demo12",
        "code": "https://github.com/demo12"
    },
    {
        "tid" : 12,
        "competition": "2023 創意競賽",
        "name": "創意設計隊",
        "student_id": "S036",
        "competition_group": "創意發想組",
        "teacher": {
            "student_id": "T017",
            "name": "林小華",
            "role": "teacher"
        },
        "team_members": [
            {"student_id": "S037", "name": "周小龍", "role": "student"}
        ],
        "description": "path/to/description/file12.pdf",
        "poster": "path/to/poster/image13.png",
        "video": None,
        "code": None
    }
]


@api.route('/api/projects/Enroll', methods=['POST'])
def register_project():
    # 接收 JSON 數據
    data = request.json
    
    # 檢查必填欄位
    required_fields = ["competition", "name", "student_id", "competition_group", "teacher", "team_members"]
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

    # 處理選填字段
    description_file = data.get("description")  # 模擬文件存儲
    poster_file = data.get("poster")  # 選填字段

    # 構建新項目數據
    new_project = {
        "tid" : len(projects) + 1,
        "competition": data["competition"],
        "name": data["name"],
        "student_id": data["student_id"],
        "competition_group": data["competition_group"],
        "teacher": teacher_account,
        "team_members": team_members,
        "description": description_file,  # 模擬存儲文件
        "poster": poster_file,  # 選填字段
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

@api.route('/api/projects/list/<year>', methods=['GET'])
def list_project(year):
    try:
        query = "SELECT * FROM project WHERE YEAR(time) = %s"
        db.cursor.execute(query, (year,))
        projects = db.cursor.fetchall()  # 取得所有資料

        # 獲取資料表的欄位名稱
        columns = [desc[0] for desc in db.cursor.description]

        # 將資料轉換為 dictionary 格式
        formatted_projects = [
            dict(zip(columns, project)) for project in projects
        ]

        # 查詢 user 資料
        user_query = "SELECT u_id, name FROM user WHERE u_id IN %s"
        all_ids = []
        for project in formatted_projects:
            all_ids.append(project["leader_id"])
            all_ids.append(project["teacher_id"])
            all_ids.extend([project.get(f"teammate{i}_id") for i in range(1, 7) if project.get(f"teammate{i}_id") is not None])

        # 去除重複的 ID
        all_ids = list(set(all_ids))

        # 查詢所有相關的使用者資料
        db.cursor.execute(user_query, (tuple(all_ids),))
        user_data = db.cursor.fetchall()
        user_map = {user[0]: user[1] for user in user_data}  # 將 u_id 映射到 name

        # 組裝返回的項目資料
        enriched_projects = []
        for project in formatted_projects:
            enriched_project = {
                "tid": project["p_id"],
                "name": project["p_name"],
                "leader": {
                    "id": project["leader_id"],
                    "name": user_map.get(project["leader_id"], "未知")
                },
                "members": [
                    {"id": project.get(f"teammate{i}_id"), "name": user_map.get(project.get(f"teammate{i}_id"), "未知")}
                    for i in range(1, 7) if project.get(f"teammate{i}_id") is not None
                ],
                "teacher": {
                    "id": project["teacher_id"],
                    "name": user_map.get(project["teacher_id"], "未知")
                },
                "video": project["video_link"],
                "github": project["github_link"]
            }
            enriched_projects.append(enriched_project)
        print(enriched_projects)
        return jsonify({"projects": enriched_projects}), 200
    except Exception as e:
        # 錯誤處理
        print(f"Error fetching projects: {e}")
        return jsonify({"message": f"Error fetching projects: {str(e)}", "error": True}), 500







ratings = {}  


@api.route('/api/projects/score', methods=['POST'])
def score_project():
    data = request.json
    tid = data.get("tid")
    ch_fla = ["創意性","實用性","美觀度","完整度"]
    # 檢查必填字段
    required_fields = ["tid", "creativity", "usability", "design", "completeness"]

    # 檢查是否有評分字段的值為 0
    zero_fields = [field for field in ["creativity", "usability", "design", "completeness"] if data[field] == 0]
    for i in range(len(zero_fields)):
        zero_fields[i]= ch_fla[zero_fields.index(zero_fields[i])]
    if zero_fields:
        return jsonify({"message": f"未填寫以下分數: {', '.join(zero_fields)}", "error": True}), 201

    # 保存評分數據
    ratings[tid] = {
        "creativity": data["creativity"],
        "usability": data["usability"],
        "design": data["design"],
        "completeness": data["completeness"]
    }
    print(ratings[tid])

    return jsonify({"message": "評分提交成功！", "ratings": ratings}), 201
