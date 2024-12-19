from pymongo import MongoClient 

from dotenv import load_dotenv
import os 

# Load environment variables from the .env file
load_dotenv()

# Access variables
DATABASE_URL = os.getenv("DATABASE_URL") 

conn = MongoClient(DATABASE_URL)
print(conn.list_database_names())

