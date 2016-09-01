def is_from_blog(record):
    return __in_value(__read_query(record), ["utm_source=blog"])


def is_robot(record):
    is_robot_agent = __in_value(__read_agent(record), [
        "Ruby",
        "Googlebot",
        "bingbot",
        "SeznamBot",
        "Baiduspider",
        "python-requests",
        "Ruby, OpenshiftUnidle",
        "MJ12bot",
        "SurveyBot",
        "Yahoo! Slurp",
        "Google-Site-Verification",
        "Go-http-client",
        "DuckDuckGo",
        "YandexBot",
        "Google Web Preview",
        "AhrefsBot",
        "bot",
        "Bot"
    ])
    is_robots_txt = __in_value(__read_path(record), ["/robots.txt"])
    return is_robot_agent or is_robots_txt


def is_index(record):
    return __in_value(__read_path(record), ["/index.html"])


def is_hack(record):
    return __read_path(record).endswith(".php")


def is_chat(record):
    return __in_value(__read_path(record), ["/chat"])


# Condition methods
def __in_value(record_value, check_parts):
    if check_parts:
        for check in check_parts:
            if check in record_value:
                return True
    return False


# Read methods

def __read_path(record):
    return __read(record, 3)


def __read_agent(record):
    return __read(record, 8)


def __read_query(record):
    return __read(record, 4)


def __read(record, number):
    res = ""
    if record and len(record) >= (number - 1):
        res = record[number]
    return res
