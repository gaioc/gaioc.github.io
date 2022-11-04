import json
import classes
import os
from uuid import uuid4
from cryptography.fernet import Fernet
import hashlib
import getpass

def clear(): #thanks GeeksForGeeks
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def create_user(name, user_list):
    user = classes.User({
        "name":name,
        "id":str(uuid4()),
        "posts":[]
    })
    user_list.user_reference[user.id] = user.to_dict()
    return user

def create_post(poster, title, content, post_list, user_list):
    post = classes.Post({
        "poster":poster,
        "title":title,
        "content":content,
        "id":str(uuid4())
    })
    user_list.user_reference[poster]["posts"].append(post.id)
    post_list.post_reference[post.id] = post.to_dict()
    return post

def pretty_post(post_list, user_list, post_id):
    post = classes.Post(post_list.post_reference[post_id])
    print('\033[1m' + post.title + '\033[0m')
    print(f"({post_id})")
    print(f"Posted by \033[1m{user_list.user_reference[post.poster]['name']}\033[0m ({user_list.user_reference[post.poster]['id']})")
    print(post.content)

def pretty_user(post_list, user_list, user_id):
    user = classes.User(user_list.user_reference[user_id])
    print('\033[1m' + user.name + '\033[0m')
    print(f"({user_id})")
    print("Posts:")
    for post_id in user.posts:
        print('\033[1m' + post_list.post_reference[post_id]["title"] + '\033[0m' + f" ({post_id})")

def pretty_posts(post_list, user_list):
    for post in post_list.post_reference.values():
        print('\033[1m' + post["title"] + f"[{user_list.user_reference[post['poster']]['name']}]\033[0m({post['id']})")

def pretty_users(user_list):
    for user in user_list.user_reference.values():
        print('\033[1m' + user["name"] + f"\033[0m({user['id']})")

posts = classes.Post_List({
    "posts":dict()
})
users = classes.User_List({
    "users":dict()
})
in_val = ""
login_uuid = None
id_key_dict = dict()
while in_val != "quit":
    posts_file = open("posts.txt", "r")
    users_file = open("users.txt", "r")
    login_file = open("login.txt", "r")
    posts.post_reference = json.loads(posts_file.read())
    users.user_reference = json.loads(users_file.read()())
    id_key_dict = json.loads(login_file.read())
    posts_file.close()
    users_file.close()
    login_file.close()
    
    print("\n\n")
    print("Not logged in" if not(login_uuid) else f"Logged in as \033[1m{users.user_reference[login_uuid]['name']}\033[0m ({login_uuid})")
    in_val = input("Enter command:")
    if in_val == "create_user" and not(login_uuid):
        user = create_user(input("Enter name:"),users)
        password = getpass.getpass()
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        id_key_dict[user.id] = json.dumps({"key":int.from_bytes(key, byteorder='big'),"salt":int.from_bytes(salt, byteorder='big')})
        print(f"User {user.name} created with UUID {user.id}")
    elif in_val == "login" and not(login_uuid):
        user_id = input("Enter user UUID:")
        password_check = getpass.getpass()
        salt = json.loads(id_key_dict[user_id])["salt"].to_bytes(32, byteorder='big')
        key_check = hashlib.pbkdf2_hmac(
            'sha256',
            password_check.encode('utf-8'),
            salt,
            100000
        )
        if key_check == json.loads(id_key_dict[user_id])["key"].to_bytes(32, byteorder='big'):
            print("Succesful login!")
            login_uuid = user_id
        else:
            print("Incorrect login information")
    elif in_val == "create_post" and login_uuid:
        post = create_post(login_uuid, input("Enter post title:"), input("Enter post content:"), posts, users)
        print(f"Post created with UUID {post.id}")
    elif in_val == "view_posts":
        pretty_posts(posts, users)
    elif in_val == "view_users":
        pretty_users(users)
    elif in_val == "view_post":
        pretty_post(posts, users, input("Enter post UUID:"))
    elif in_val == "view_user":
        pretty_user(posts, users, input("Enter user UUID:"))
    elif in_val == "clear_data":
        posts.post_reference = dict()
        users.user_reference = dict()
        id_key_dict = dict()
        print("All clear!")
    elif in_val == "logout" and login_uuid:
        login_uuid = None
        print("Successfully logged out!")

    posts_file = open("posts.txt", "w")
    users_file = open("users.txt", "w")
    login_file = open("login.txt", "w")
    db["posts"] = json.dumps(posts.post_reference)
    db["users"] = json.dumps(users.user_reference)
    db["login"] = json.dumps(id_key_dict)
    
