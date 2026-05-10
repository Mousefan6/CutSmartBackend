from flask import Blueprint, request, jsonify
import jwt

from server.services.history_service import add_history
from server.utils.config import SECRET_KEY

history_bp = Blueprint("history", __name__)

@history_bp.route("/create", methods=["POST"])
def create_history():
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({
                "success": False,
                "message": "Missing authorization header"
            }), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "message": "Invalid authorization format"
            }), 401

        token = auth_header.split(" ")[1]

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        user_id = payload["user_id"]

        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Missing request body"
            }), 400

        history = add_history(user_id, data)

        return jsonify({
            "success": True,
            "message": "History created successfully",
        }), 201
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
