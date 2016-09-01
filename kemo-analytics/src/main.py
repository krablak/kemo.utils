import subprocess
import tempfile
import os
from os import listdir
from os.path import isfile, join
import collections
import traceback

import rules
import utils
from structures import DayStat


def main():
    app_name = "kemoundertow"
    target_dir = tempfile.mkdtemp()
    data_js_file_name = "%s/html/js/data.js" % os.path.dirname(os.path.abspath(__file__))

    # Download log files
    for log_file in utils.logs_history(40):
        log_file = "app-root/logs/%s" % log_file
        subprocess.call(["rhc", "scp", app_name, "download", target_dir, log_file])

    # Day base statistics holder
    day_stats = {}
    # Last 100 requests
    last_requests = collections.deque([], 100)
    # User agents
    user_agents = set()

    # Function storing user agents in set
    def add_user_agent(record):
        user_agents.add(record[8])

    # Save data from log files
    for log_file in listdir(target_dir):
        log_file_path = join(target_dir, log_file)
        if isfile(log_file_path):
            print "Processing file: %s" % log_file_path
            parse_and_save(log_file_path, day_stats, [last_requests.append, add_user_agent])

    # Create JS data file
    with open(data_js_file_name, 'w') as js_file:
        data = day_stats.values()
        data = list(sorted(data, key=lambda stat: stat.datetime))
        js_file.write("var stats_data = %s;\n" % utils.ObjectEncoder().encode(data))
        js_file.write("var last_requests = %s;\n" % utils.ObjectEncoder().encode(list(reversed(last_requests))))
        js_file.write("var user_agents = %s;\n" % utils.ObjectEncoder().encode(list(user_agents)))


def save_record(record, day_stats):
    try:
        date_str = record[0]
        day_stat = None
        if date_str in day_stats:
            day_stat = day_stats[date_str]
        else:
            day_stat = DayStat(date_str)
            day_stats[date_str] = day_stat

        # Count all requests
        day_stat.all_count += 1

        if rules.is_robot(record):
            # Count request made by robots and crawlers
            day_stat.robot_count += 1
        elif rules.is_hack(record):
            # Count various lookups for security holes
            day_stat.hack_count += 1
        else:
            # User page requests
            day_stat.user_stat.update(index=rules.is_index(record),
                                      chat=rules.is_chat(record),
                                      is_from_blog=rules.is_from_blog(record))
    except Exception, e:
        print str(e)
        traceback.print_exc()


def parse_and_save(log_file_path, day_stats, on_record_fns):
    with open(log_file_path) as f:
        for line in f:
            record = line.split("\t")
            for record_fn in on_record_fns:
                record_fn(record)
            save_record(record, day_stats)


if __name__ == "__main__":
    main()
