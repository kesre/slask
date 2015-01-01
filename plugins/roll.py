"""!roll [<number>][d<size>]. eg 1d6 or d20. Roll dice. Defaults to 1d6"""
import random
import re

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!roll( (\d*)d?(\d*))?$", text)
    if match:
        number = int(match[0][1]) if match[0][1] else 1
        size = int(match[0][2]) if match[0][2] else 6
        return ", ".join([
            str(random.randint(1, size))
            for _ in xrange(number)
        ])
    return ""