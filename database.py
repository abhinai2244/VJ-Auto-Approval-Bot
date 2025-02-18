from pymongo import MongoClient
from configs import cfg

# Connect to MongoDB
client = MongoClient(cfg.MONGO_URI)

# Define the collections for users and groups
users = client['main']['users']
groups = client['main']['groups']

# Check if a user is already in the database
def already_db(user_id):
    user = users.find_one({"user_id": str(user_id)})
    return user is not None

# Check if a group is already in the database
def already_dbg(chat_id):
    group = groups.find_one({"chat_id": str(chat_id)})
    return group is not None

# Add a user to the database
def add_user(user_id):
    if not already_db(user_id):
        return users.insert_one({"user_id": str(user_id)})

# Remove a user from the database
def remove_user(user_id):
    if already_db(user_id):
        return users.delete_one({"user_id": str(user_id)})

# Add a group to the database
def add_group(chat_id):
    if not already_dbg(chat_id):
        return groups.insert_one({"chat_id": str(chat_id)})

# Get the total number of users
def all_users():
    return users.count_documents({})  # Use count_documents for more efficiency

# Get the total number of groups
def all_groups():
    return groups.count_documents({})  # Use count_documents for more efficiency
