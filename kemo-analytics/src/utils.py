import datetime

from json import JSONEncoder
from structures import DayStat, UserStat


class ObjectEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, DayStat) or isinstance(o, UserStat):
            return o.__dict__
        elif isinstance(o, datetime.datetime):
            return o.strftime("%Y_%m_%d")
        else:
            return o


def logs_history(days=1):
    """
    Provides generator with log file names for given number of days in history.
    :param days: number of files in history to provide.
    :return: ready to use log file names generator.
    """
    # History time delta in days
    day_delta = 0

    while day_delta <= days:
        # Prepare new datetime in history from current time and delta value
        cur_datetime = datetime.datetime.now() + datetime.timedelta(days=-day_delta)
        # Return and yield log filename based on computed datetime
        yield "access_%s.log" % cur_datetime.strftime("%Y_%m_%d")
        day_delta += 1