from selenium import webdriver
import os
import logging
import sys

import tumblr.api
import tumblr.data

# Setup basic logging
logger = logging.getLogger('like_bot_main')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# Path to phantom js MacOS binary
phantom_js_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../phantomjs-2.1.1-macosx/bin/phantomjs")


def main():
    logger.info('Running Tumblr Like crawler')
    login = sys.argv[1]
    password = sys.argv[2]

    # Prepare crawling api and login
    tumblr_api = tumblr.api.TumblrApi()
    tumblr_api.login(login, password)

    # Posts classification
    import datasets.simple
    learned = {
        'programming': datasets.simple.programming,
        'security': datasets.simple.security,
        'messaging': datasets.simple.messaging,
        'art': datasets.simple.art,
        'porn': datasets.simple.porn,
        'krablak_following': datasets.simple.krablak_following,
        'other': datasets.simple.other,
    }

    # Local actions history storage
    storage = tumblr.data.PostsStorage()
    # Posts likes storage
    likes_storage = tumblr.data.LikesStorage()

    # Counter of likes per run
    likes_per_run = Counter()

    # Function called on crawled post
    def on_post(driver, element, post):
        # On post default result
        on_post_res = tumblr.api.OnPostCommand.nop()
        if likes_per_run.reached_max():
            logger.debug("Max number of %s likes was reached. Stopping.", likes_per_run.max_count)
            on_post_res = tumblr.api.OnPostCommand.stop()
        else:
            # classify post content
            bayes_res = datasets.classify(post.content, learned)
            # logger.debug("Result '%s' for '%s'", datasets.to_str(bayes_res), post.content.replace("\n"," "))
            liked = False
            if "programming" == bayes_res.most_likely() and not likes_storage.is_liked(post):
                likes_per_run.inc()
                likes_storage.like(post)
                # Mark for liking
                on_post_res = tumblr.api.OnPostCommand.like()
                liked = True
            logger.debug("%5s %5s %13s: %s", liked, post.notes_count, bayes_res.most_likely(),
                         post.content.replace("\n", " "))
        # By default do not like post
        return on_post_res

    # Run searches
    tumblr_api.search(phrase="computer", on_post_fn=on_post)
    if not likes_per_run.reached_max():
        tumblr_api.search(phrase="programming", on_post_fn=on_post)
    if not likes_per_run.reached_max():
        tumblr_api.search(phrase="java programming", on_post_fn=on_post)
    if not likes_per_run.reached_max():
        tumblr_api.search(phrase="python programming", on_post_fn=on_post)

        # storage = tumblr.data.PostsStorage()
        # posts = storage.load_all()


class Counter():
    def __init__(self, max_count=10):
        self.max_count = max_count
        self.count = 0

    def inc(self):
        self.count = self.count + 1

    def reached_max(self):
        return self.max_count < self.count


if __name__ == '__main__':
    main()
