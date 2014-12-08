"""!backtothefuture <date> returns the delorean dashboard with the specified <date>"""

import re
import parsedatetime


p = parsedatetime.Calendar()


def backtothefutureday(datestr):
    dt = p.parse(datestr)[0]
    return 'http://www.itsbacktothefutureday.com/images/{year}/{month}/{day}.jpg'.format(year=dt.tm_year, month=dt.tm_mon, day=dt.tm_mday)


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!backtothefuture (.*)", text)
    if match:
        return backtothefutureday(match[0])
