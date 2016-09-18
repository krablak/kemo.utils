import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import logging
import urllib.parse
import re

# Setup basic logging
logger = logging.getLogger('tumblr_api')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# Path to phantom js MacOS binary
phantom_js_path = os.path.join(os.path.dirname(
    os.path.realpath(__file__)),
    os.pardir,
    os.pardir,
    "phantomjs-2.1.1-macosx/bin/phantomjs")

screenshots_path = os.path.join(os.path.dirname(
    os.path.realpath(__file__)),
    os.pardir,
    os.pardir,
    "screenshots")


class TumblrPost:
    def __init__(self):
        self.data_id = ""
        self.user = ""
        self.data_type = ""
        self.tags = []
        self.content = ""
        self.notes_count = 0

    def __str__(self):
        return "TumblrPost[data_id:%s,user:%s,data_type:%s,notes_count:%s]" % (
            self.data_id, self.user, self.data_type, self.notes_count)


class OnPostCommand():
    """
    Command representing actions to be done after post processing by "on_post" function.
    """

    def __init__(self, like=False, stop=False):
        # Like post
        self.like = like
        # Stop after this command
        self.stop = stop

    @staticmethod
    def like():
        return OnPostCommand(like=True, stop=False)

    @staticmethod
    def stop():
        return OnPostCommand(like=False, stop=True)

    @staticmethod
    def nop():
        return OnPostCommand(like=False, stop=False)


def _empty_on_post(driver, element, post):
    return OnPostCommand.nop()


class TumblrApi:
    def __init__(self):
        # Prepare selenium instance
        self.driver = webdriver.PhantomJS(executable_path=phantom_js_path)
        self.driver.set_window_size(1280, 800)

    def login(self, login, password):
        logger.debug("Logging into tumblr using login %s and password ******", login)
        # Perform basic logout
        self.driver.get("https://www.tumblr.com/logout")
        # Wait for login form
        logger.debug("Waiting for email form...")
        login_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "signup_determine_email"))
        )
        self.driver.get_screenshot_as_file(os.path.join(screenshots_path, "filled-login-0.png"))

        # Fill login
        login_input.send_keys(login)
        self.driver.get_screenshot_as_file(os.path.join(screenshots_path, "filled-login-1.png"))

        # Submit filled login
        submit_login_btn = self.driver.find_element_by_id("signup_forms_submit")
        submit_login_btn.click()

        # Wait for password input
        logger.debug("Waiting for password form...")
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "signup_password"))
        )
        password_input.send_keys(password)
        self.driver.get_screenshot_as_file(os.path.join(screenshots_path, "filled-login-2.png"))

        # Click on login button
        submit_login_btn.click()
        logger.debug("Login button clicked. Waiting for dashboard.")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "account_button"))
        )
        self.driver.get_screenshot_as_file(os.path.join(screenshots_path, "filled-login-3.png"))
        logger.debug("We are logged in!")

    def is_logged(self):
        return self.driver.find_element_by_id("account_button") is not None

    def search(self, phrase="all", on_post_fn=_empty_on_post):
        logger.debug("Searching posts for '%s'", phrase)

        # Perform basic logout
        self.driver.get("https://www.tumblr.com/search/%s" % urllib.parse.quote(phrase))
        # Wait for search results
        logger.debug("Waiting for search results...")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "account_button"))
        )
        self.driver.get_screenshot_as_file(os.path.join(screenshots_path, "search-0.png"))

        # Scroll down for next pages
        self._scroll_down(scroll_attempts=5)

        # Get search result
        search_res_arts = self.driver.find_elements_by_tag_name("article")
        self.driver.get_screenshot_as_file(os.path.join(screenshots_path, "search-1.png"))

        for cur_art in search_res_arts:
            cur_post = search_article_to_post(cur_art)
            on_post_res = on_post_fn(driver=self.driver, element=cur_art, post=cur_post)
            if on_post_res.stop:
                break
            elif on_post_res.like:
                like_btns = cur_art.find_elements_by_class_name("like")
                if like_btns:
                    like_btns[0].click()
                else:
                    logger.warn("Cannot find like button for post: %s", cur_post)

    def blog_posts(self, blog_id="techkrab", on_post_fn=_empty_on_post):
        logger.debug("Loading blog posts for: '%s'", blog_id)
        self.driver.get("https://www.tumblr.com/dashboard/blog/%s" % urllib.parse.quote(blog_id))
        # Wait for search results
        logger.debug("Waiting for search results...")
        blog_dash_elem = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "indash_blog"))
        )
        blog_dash_elem.click()

        # Scroll down for next pages
        self._scroll_down(scroll_attempts=5, loader_class="knight-rider-loader")

        # Get search result
        blog_posts_elems = blog_dash_elem.find_elements_by_class_name("post")

        for cur_art in blog_posts_elems:
            cur_post = _blog_div_to_post(cur_art, self.driver)
            on_post_fn(driver=self.driver, element=cur_art, post=cur_post)

    def _scroll_down(self, scroll_attempts=2, loader_class="Knight-Rider-loader"):
        logger.debug("Scrolling down for more results...")
        while scroll_attempts > 0:
            logger.debug("Scrolling results page %s", scroll_attempts)
            # Scroll down for next pages
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logger.debug("Scrolled down")
            try:
                # Wait for paging indicator
                loading_ind_elem = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, loader_class))
                )
                if not loading_ind_elem:
                    logger.debug("Page has no more results")
                    break
                # Wait for end of page loading
                WebDriverWait(self.driver, 20).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, loader_class))
                )
                scroll_attempts -= 1
            except TimeoutException as e:
                logger.debug("One of searched loading indicators was not found. Page has no more data.")
                break


def search_article_to_post(search_article_element):
    # Ugly hack for "not yet loaded async elements"
    if search_article_element.text == '':
        search_article_element.click()

    post = TumblrPost()
    post.data_id = search_article_element.get_attribute("data-id")
    post.user = search_article_element.get_attribute("data-tumblelog")
    post.data_type = search_article_element.get_attribute("data-type")
    post_tags = search_article_element.find_elements_by_class_name("post_tag")
    for cur_post_tag in post_tags:
        post.tags.append(cur_post_tag.get_attribute("data-tag"))

    search_article_element.is_displayed()
    post_content_elem = search_article_element.find_element_by_class_name("post_content")
    if post_content_elem and post_content_elem.text:
        post.content = post_content_elem.text

    note_link_elem = search_article_element.find_element_by_class_name("note_link_current")
    if note_link_elem:
        post.notes_count = int(note_link_elem.get_attribute("data-count"))

    return post


def _blog_div_to_post(blog_div, driver):
    # Ugly hack for "not yet loaded async elements"
    if blog_div.text == '':
        blog_div.click()

    post = TumblrPost()
    post.data_id = blog_div.get_attribute("data-post-id")
    post.user = blog_div.get_attribute("data-tumblelog-name")

    def to_data_type(blog_div):
        classes = blog_div.get_attribute("class").split()
        if "is_text":
            return "text"
        if "is_video":
            return "video"
        if "is_photo":
            return "photo"
        else:
            return "unknown"

    post.data_type = to_data_type(blog_div)

    post_tags = blog_div.find_elements_by_class_name("post_tag")
    for cur_post_tag in post_tags:
        post.tags.append(cur_post_tag.get_attribute("data-tag"))

    post_content_elems = blog_div.find_elements_by_class_name("post_content")
    if post_content_elems and post_content_elems[0].text:
        post.content = post_content_elems[0].text

    note_link_elems = blog_div.find_elements_by_class_name("note_link_current")
    if note_link_elems:
        post.notes_count = int(note_link_elems[0].get_attribute("data-count"))

    return post
