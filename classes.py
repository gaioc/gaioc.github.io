class User:
    def __init__(self, info_dict):
        self.name = info_dict["name"] # On-screen name
        self.id = info_dict["id"] # user UUID
        self.posts = info_dict["posts"] # list of UUIDs
    def to_dict(self):
        return {
            "name":self.name, 
            "id":self.id,
            "posts":self.posts
        }

class Post:
    def __init__(self, info_dict):
        self.title = info_dict["title"] # post title
        self.id = info_dict["id"] # post UUID
        self.content = info_dict["content"] # post content
        self.poster = info_dict["poster"] # poster UUID
    def to_dict(self):
        return {
            "title":self.title,
            "id":self.id,
            "content":self.content,
            "poster":self.poster
        }
class Post_List:
    def __init__(self, info_dict):
        self.post_reference = info_dict["posts"] # dict of UUID to post
    def to_dict(self):
        return {"posts": self.post_reference}

class User_List:
    def __init__(self, info_dict):
        self.user_reference = info_dict["users"] # dict of UUID to user
    def to_dict(self):
        return {"users": self.user_reference}

