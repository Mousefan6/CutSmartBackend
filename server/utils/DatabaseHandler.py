from pymongo import MongoClient

from server.utils.config import (
    MONGO_URL,
    CUTSMART_DB,
    USERS_COLLECTION,
    HISTORY_COLLECTION,
)

class DatabaseHandler:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.cutsmart_db = self._get_or_init_db(CUTSMART_DB)

        self._ensure_collections(self.cutsmart_db)

    def _get_or_init_db(self, db_name: str):
        if not db_name in self.client.list_database_names():
            print(f"[!] Database '{db_name}' does not exist yet. Initializing...")
            # Force create by inserting a dummy doc and then removing it
            temp_db = self.client[db_name]
            temp_db["__init__"].insert_one({"init": True})
            temp_db.drop_collection("__init__")
            print(f"[+] Database '{db_name}' created.")

        return self.client[db_name]

    def _ensure_collections(self, db):
        existing_collections = db.list_collection_names()

        if USERS_COLLECTION not in existing_collections:
            print(f"[+] Creating collection: users in {db.name}")
            db.create_collection(USERS_COLLECTION)

        if HISTORY_COLLECTION not in existing_collections:
            print(f"[+] Creating collection: history in {db.name}")
            db.create_collection(HISTORY_COLLECTION)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
