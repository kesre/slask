"""!backtothefuture <date> returns the delorean dashboard with the specified <date>"""

import re
import time

import parsedatetime
p = parsedatetime.Calendar()


def backtothefutureday(datestr):
    dt, result = p.parse(datestr)
    if result == 0:
        return "I'm not eating that bogus date."
    if not isinstance(dt, time.struct_time):
        if len(dt) != 9:
            return 'Could not extrapolate date values from parsed date. Your date smells bogus.'
        dt = time.struct_time(dt)
    year, month, day = dt.tm_year, dt.tm_mon, dt.tm_mday
    return 'http://www.itsbacktothefutureday.com/images/{year}/{month:02d}/{day:02d}.jpg'.format(year=year, month=month, day=day)


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!backtothefuture (.*)", text)
    if match:
        return backtothefutureday(match[0])
