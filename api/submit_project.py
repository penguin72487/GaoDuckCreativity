from flask import Blueprint, jsonify, request
from api.sql_connection import SqlAPI

db = SqlAPI()
api = Blueprint('submit_project_api', __name__)

@api.route('/api/submit_project', methods=['POST'])
def submit_project():
    data = request.json

    leader_id = data.get("student_id")
    teammate2_id = data.get("team_member1")
    teammate3_id = data.get("team_member2")
    teammate4_id = data.get("team_member3")
    teammate5_id = data.get("team_member4")
    teammate6_id = data.get("team_member5")
    teacher_id = data.get("teacher_id")
    p_name = data.get("name")
    description_file = data.get("description")
    poster_file = data.get("poster")
    video_link = data.get("video")
    github_link = data.get("code")

    result = db.submitproject(leader_id, teammate2_id, teammate3_id, teammate4_id, teammate5_id, teammate6_id, teacher_id, p_name, description_file, poster_file, video_link, github_link)
    
    if result == "succ":
        return jsonify({"message": "項目提交成功"}), 200
    else:
        return jsonify({"message": result}), 400