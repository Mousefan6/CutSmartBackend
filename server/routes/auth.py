from bson import ObjectId
import jwt
import datetime
from flask import Blueprint, jsonify, request
from server.utils.DatabaseHandler import DatabaseHandler
from server.utils.config import SECRET_KEY

auth_bp = Blueprint('auth_bp', __name__)

# --- LOGIN ROUTE ---
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"success": False, "message": "Missing credentials"}), 400

        with DatabaseHandler() as db:
            # Finding user where the field "user" matches the input username
            user = db.cutsmart_db["users"].find_one({"user": username})

            if user and user.get("password") == password:
                # Create JWT Token
                payload = {
                    "user_id": str(user["_id"]),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

                return jsonify({
                    "success": True,
                    "message": "Login successful",
                    "session_token": token
                }), 200
            else:
                return jsonify({"success": False, "message": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# --- PROFILE ROUTE ---
@auth_bp.route("/profile", methods=["GET"])
def profile_route():
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "success": False,
                "message": "Missing token"
            }), 401

        token = auth_header.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]

        with DatabaseHandler() as db:
            user = db.cutsmart_db["users"].find_one({
                "_id": ObjectId(user_id)
            })

            if not user:
                return jsonify({
                    "success": False,
                    "message": "User not found"
                }), 404

            return jsonify({
                "success": True,
                "username": user.get("user"),
                "email": user.get("email", "not set")
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

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not password or not email:
            return jsonify({"success": False, "message": "Missing fields"}), 400

        with DatabaseHandler() as db:
            # Check if user already exists
            existing_user = db.cutsmart_db["users"].find_one({"user": username})
            if existing_user:
                return jsonify({"success": False, "message": "User already exists"}), 409

            # Insert new user
            new_user = {
                "user": username,
                "email": email,
                "password": password, # In production, use hashing like werkzeug.security
                "created_at": datetime.datetime.utcnow()
            }
            result = db.cutsmart_db["users"].insert_one(new_user)

            # Create token immediately so they are "logged in" after registering
            payload = {
                "user_id": str(result.inserted_id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return jsonify({
                "success": True,
                "message": "User registered",
                "session_token": token
            }), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
