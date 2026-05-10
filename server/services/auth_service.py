import bcrypt
import jwt
from bson import ObjectId
from datetime import datetime, timezone, timedelta

from server.utils.DatabaseHandler import DatabaseHandler
from server.utils.config import SECRET_KEY

def register(username: str, password: str):
    try:
        with DatabaseHandler() as db:
            user_collection = db.cutsmart_db["users"]

            existing_user = user_collection.find_one({
                "user": username
            })
            if existing_user:
                raise ValueError("User already exists")

            credential = {
                "user": username,
                "password": hash_password(password),
            }

            user_collection.insert_one(credential)
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

def hash_password(hash_string: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(hash_string.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def login(username: str, password: str):
    try:
        with DatabaseHandler() as db:
            user_collection = db.cutsmart_db["users"]

            user = user_collection.find_one({
                "user": username
            })

            if not user:
                return {
                    "success": False,
                    "message": "Invalid credentials"
                }

            stored_hash = user["password"]

            password_matches = bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash.encode("utf-8")
            )
            if not password_matches:
                return {
                    "success": False,
                    "message": "Invalid credentials"
                }

            # Create JWT token with a TTL of 1 day
            token = jwt.encode(
                {
                    "user_id": str(user["_id"]),
                    "exp": datetime.now(timezone.utc) + timedelta(days=1)
                },
                SECRET_KEY,
                algorithm="HS256"
            )

            # Store the session token in the user collection.
            # Use to invalidate sessions when user logs out or changes password.
            user_collection.update_one(
                {
                    "_id": user["_id"]
                },
                {
                    "$set": {
                        "session_token": token
                    }
                }
            )

            return {
                "success": True,
                "message": "Login successful",
                "session_token": token
            }
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

def logout(token: str):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"]
    )

    user_id = payload["user_id"]

    with DatabaseHandler() as db:
        user_collection = db.cutsmart_db["users"]
        user_collection.update_one(
            {
                "_id": ObjectId(user_id)
            },
            {
                "$unset": {
                    "session_token": ""
                }
            }
        )
