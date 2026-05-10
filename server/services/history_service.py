from server.utils.DatabaseHandler import DatabaseHandler
from datetime import datetime

def get_history(user_id: str) -> list:
    try:
        with DatabaseHandler() as db:
            history_collection = db.cutsmart_db["history"]

            history = list(history_collection.find({
                "user_id": user_id
            }))

            for item in history:
                item["_id"] = str(item["_id"])

            return history
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

def add_to_history(user_id, food_name, nutrition):
    with DatabaseHandler() as db:
        history_collection = db.user_db["history"]

        entry = {
            "user_id": user_id,
            "name": food_name,
            "nutrition": nutrition,
            "isSaved": False, # Matches your HistoryPage logic
            "timestamp": datetime.utcnow()
        }

        history_collection.insert_one(entry)
