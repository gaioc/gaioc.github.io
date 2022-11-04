import json
import classes
import os
from uuid import uuid4
from cryptography.fernet import Fernet
import hashlib
import getpass
import sys

def create_user(name, user_list):
    user = classes.User({
        "name":name,
        "id":str(uuid4()),
        "posts":[]
    })
    user_list.user_reference[user.id] = user.to_dict()
    return user

  
users = classes.User_List({
    "users":dict()
})
users_file = open("users.txt", "r")
users.user_reference = json.loads(users_file.read())
users_file.close()


user = create_user(sys.argv[1],users)
password = sys.argv[2]
salt = os.urandom(32)
key = hashlib.pbkdf2_hmac(
    'sha256',
    password.encode('utf-8'),
    salt,
    100000
)
id_key_dict[user.id] = json.dumps({"key":int.from_bytes(key, byteorder='big'),"salt":int.from_bytes(salt, byteorder='big')})
print(f"User {user.name} created with UUID {user.id}")


users_file = open("users.txt", "w")
users_file.write(json.dumps(users.user_reference))
users_file.close()
