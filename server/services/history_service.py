from datetime import datetime

from server.utils.DatabaseHandler import DatabaseHandler

def add_history(user_id: str, history_data: dict) -> None:
    try:
        with DatabaseHandler() as db:
            history_collection = db.cutsmart_db["history"]

            history_document = {
                "user_id": user_id,
                "name": history_data.get("name"),
                "cutting_safety_tips": history_data.get("cutting_safety_tips"),
                "nutritional_facts_per_100g": history_data.get("nutritional_facts_per_100g"),
                "created_at": datetime.utcnow()
            }

            history_collection.insert_one(history_document)
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")
