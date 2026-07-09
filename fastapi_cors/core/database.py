from pymongo import AsyncMongoClient

client = AsyncMongoClient("mongodb+srv://vkalpanasharma00_db_user:XJMdJxu50KJZ3ieK@cluster0.nml3k20.mongodb.net/")

db = client["mydatabase"]

user_collection = db["users"]