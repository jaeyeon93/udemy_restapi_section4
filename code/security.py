# -*- coding:utf-8 -*-

from werkzeug.security import safe_str_cmp # safe string compare
from user import User
users = [
   User(1,'bob','asdf')
]

#
# username_mapping = { u.username : u for u in users}
# userid_mapping = {u.id: u for u in users}
#
#
# userid_mapping = {1 : {
#         'id' :1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# }

# def authenticate(username, password):
#     user = userid_mapping.get(username, None)
#     if user and safe_str_cmp(password, password):
#         return user
#
# def identity(payload):
#     # payload is a content jwt tokken extract userid?
#     user_id = payload['identity']
#     return userid_mapping.get(user_id,None)

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)