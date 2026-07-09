from pymongo import AsyncMongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE = os.getenv("database_name")

client = AsyncMongoClient(MONGO_URI)

db = client[DATABASE]

user_collection = db["users"]