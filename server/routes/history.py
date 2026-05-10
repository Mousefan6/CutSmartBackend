from flask import Blueprint, request, jsonify
import jwt

from server.services.history_service import get_history
from server.utils.config import SECRET_KEY

history_bp = Blueprint("history", __name__)

@history_bp.route("/", methods=["GET"])
def get_history():
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({
                "success": False,
                "message": "Missing authorization header"
            }), 401

        token = auth_header.split(" ")[1]

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        user_id = payload["user_id"]

        history = get_history(user_id)

        return jsonify({
            "success": True,
            "history": history
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({
            "success": False,
            "message": "Token expired"
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            "success": False,
            "message": "Invalid token"
        }), 401
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
