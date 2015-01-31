"""!md5 <phrase> return an md5 hash for <phrase>"""

import md5
import re

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!md5 (.*)", text)
    if not match: return

    return md5.md5(match[0]).hexdigest()
