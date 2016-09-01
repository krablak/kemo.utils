import datetime

class UserStat:
    def __init__(self):
        self.index_count = 0
        self.chat_count = 0
        self.from_blog_count = 0
        self.user_count = 0

    def update(self, index=False, chat=False, is_from_blog=False):
        self.user_count += 1
        if index:
            self.index_count += 1
        elif chat:
            self.chat_count += 1
        if is_from_blog:
            self.from_blog_count += 1

    def __str__(self):
        return "{index_count=%s chat_count=%s from_blog_count=%s}" % (
            self.index_count, self.chat_count, self.from_blog_count)


class DayStat:
    def __init__(self, day):
        # Day name
        self.day = day
        # Ordering datetime value
        self.datetime = datetime.datetime.strptime(day, "%Y-%m-%d")
        # Count of all requests (pages & resources)
        self.all_count = 0
        # Count of robots requests
        self.robot_count = 0
        # Count of hack attempts requests
        self.hack_count = 0
        # User request stats
        self.user_stat = UserStat()

    def __str__(self):
        return "{day=%s all_count=%s user_stat=%s}" % (self.day, self.all_count, self.user_stat)

