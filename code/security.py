from werkzeug.security import safe_str_cmp
from resources.user import User

# werkzeug.security safe_str_cmp accounts for different String encodings before comparisons (eg. ascii, utf-8)

def authenticate(username, password):
  user = User.find_by_username(username)
  if user and safe_str_cmp(user.password, password):
    return user

def identity(payload):
  user_id = payload['identity']
  return User.find_by_id(user_id)