from flask import Blueprint, jsonify, request
from flask_cors import CORS
from api.sql_connection import SqlAPI
import logging

db = SqlAPI()
announcement_api = Blueprint('announcement_api', __name__)
CORS(announcement_api, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# 設置日誌記錄
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

@announcement_api.route('/api/announcements', methods=['POST'])
def post_announcement():
    try:
        data = request.json
        title = data.get("title")
        information = data.get("content")
        publisher_u_id = data.get("publisher_u_id")

        if not title or not information or not publisher_u_id:
            return jsonify({"message": "缺少必要的公告信息"}), 400

        # 檢查 `publisher_u_id` 是否存在於 `user` 表
        db.cursor.execute("SELECT COUNT(*) FROM user WHERE u_id = %s", (publisher_u_id,))
        if db.cursor.fetchone()[0] == 0:
            return jsonify({"message": "發佈者 ID 無效，請確認該用戶是否存在"}), 400

        result = db.postannouncement(title, information, publisher_u_id)
        return jsonify({"message": result}), 201
    except Exception as e:
        logger.error(f"Error posting announcement: {e}")
        return jsonify({"message": f"Error posting announcement: {str(e)}"}), 500


@announcement_api.route('/api/announcements/<int:a_id>', methods=['PUT'])
def modify_announcement(a_id):
    try:
        data = request.json
        title = data.get("title")
        information = data.get("content")
        publisher_u_id = data.get("publisher_u_id")

        if not title or not information or not publisher_u_id:
            raise ValueError("缺少必要的公告信息")

        result = db.modiannouncement(a_id, title, information, publisher_u_id)
        return jsonify({"message": result}), 200
    except Exception as e:
        logger.error(f"Error modifying announcement: {e}")
        return jsonify({"message": f"Error modifying announcement: {str(e)}"}), 500

@announcement_api.route('/api/announcements/<int:a_id>', methods=['DELETE'])
def delete_announcement(a_id):
    try:
        result = db.deleteannouncement(a_id)
        return jsonify({"message": result}), 200
    except Exception as e:
        logger.error(f"Error deleting announcement: {e}")
        return jsonify({"message": f"Error deleting announcement: {str(e)}"}), 500

@announcement_api.route('/api/announcements', methods=['GET'])
def get_announcements():
    try:
        number = request.args.get('number', default=10, type=int)
        offset = request.args.get('offset', default=0, type=int)
        results = db.getannouncementlist(number, offset)

        return jsonify({"announcements": results}), 200  # ✅ 確保回傳的是 JSON 格式
    except Exception as e:
        logger.error(f"Error fetching announcements: {e}")
        return jsonify({"message": f"Error fetching announcements: {str(e)}"}), 500



@announcement_api.route('/api/announcements/<int:a_id>', methods=['GET'])
def get_announcement_detail(a_id):
    try:
        result = db.getannouncementdetail(a_id)
        if result:
            announcement = {
                "title": result[0],
                "publisher_u_id": result[1],
                "content": result[2],
                "publish_timestamp": result[3],
                "last_update_timestamp": result[4]
            }
            return jsonify({"announcement": announcement}), 200
        else:
            return jsonify({"message": "公告未找到"}), 404
    except Exception as e:
        logger.error(f"Error fetching announcement detail: {e}")
        return jsonify({"message": f"Error fetching announcement detail: {str(e)}"}), 500