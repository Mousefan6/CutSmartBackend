from dotenv import load_dotenv

load_dotenv();

# MongoDB configuration
MONGO_URI = "mongodb://mongo:27017"
CUTSMART_DB = "CutSmart"
USERS_COLLECTION = "users"
HISTORY_COLLECTION = "history"

# Secrets
SECRET_KEY = "ratatouille-remy-the-rat"
