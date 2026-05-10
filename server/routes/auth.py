from flask import Blueprint, request, jsonify
import jwt

from server.services.auth_service import register, login, logout

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Missing request body"
            }), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "success": False,
                "message": "Username and password required"
            }), 400

        register(username, password)

        return jsonify({
            "success": True,
            "message": "User registered successfully"
        }), 201
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 409
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@auth_bp.route("/login", methods=["POST"])
def login_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Missing request body"
            }), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "success": False,
                "message": "Username and password required"
            }), 400

        result = login(username, password)

        if result["success"]:
            return jsonify(result), 200

        return jsonify(result), 401
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({
                "success": False,
                "message": "Missing authorization header"
            }), 401

        token = auth_header.split(" ")[1]

        logout(token)

        return jsonify({
            "success": True,
            "message": "Logged out successfully"
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
