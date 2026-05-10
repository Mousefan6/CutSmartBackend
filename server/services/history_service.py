from server.utils.DatabaseHandler import DatabaseHandler

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
