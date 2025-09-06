import time
import re
import json
from collections import defaultdict
import re
import os


USER_FILE = "user.json"
OWNER_ID = 6045936701  #

RATE_LIMIT_SECONDS = 0 if OWNER_ID == 6045936701 else 15

user_last_message = defaultdict(float)

def is_rate_limited(user_id):
    current_time = time.time()
    if current_time - user_last_message[user_id] < RATE_LIMIT_SECONDS:
        return True
    user_last_message[user_id] = current_time
    return False

def is_valid_url(url):
    pattern = r'^https?://[^\s]+$'
    return re.match(pattern, url) is not None

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def is_registered(user_id):
    users = load_users()
    return users.get(str(user_id), {}).get("registered", False)

def get_role(user_id):
    users = load_users()
    return users.get(str(user_id), {}).get("role", "free")

def set_role(user_id, role):
    users = load_users()
    users[str(user_id)] = {"registered": True, "role": role}
    save_users(users)

def register_user(user_id):
    if not is_registered(user_id):
        set_role(user_id, "free")
        
def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
        
def has_permission(user_id, required_role):
    role_hierarchy = {"free": 1, "premium": 2, "admin": 3, "owner": 4}
    user_role = get_role(user_id)
    return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)    
    
