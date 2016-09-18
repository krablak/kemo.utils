from tumblr.api import TumblrPost
import os.path
import tinydb
import time


class PostsStorage:
    def __init__(self):
        data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../data/posts.json")
        self.db = tinydb.TinyDB(data_file)

    def save(self, post):
        self.db.insert(post_to_json(post))

    def load_all(self):
        posts_json = self.db.all()
        return map(json_to_post, posts_json)


class LikesStorage:
    def __init__(self):
        data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../data/likes.json")
        self.db = tinydb.TinyDB(data_file)

    def like(self, post):
        self.db.insert({"data_id": post.data_id, "liked": True, "date": time.time()})

    def is_liked(self, post):
        like_data = self.db.search(tinydb.where("data_id") == post.data_id)
        return like_data and like_data[0]["liked"]


def post_to_json(post):
    return post.__dict__


def json_to_post(json_dict):
    post = TumblrPost()
    for key, value in json_dict.items():
        post.__dict__[key] = value
    return post
