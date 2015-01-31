"""!md5 <phrase> return an md5 hash for <phrase>"""

import md5
import re

def on_message(msg, server):
    """

    >>> on_message({"text": "!md5 asdf"}, None)
    '912ec803b2ce49e4a541068d495ab570'

    """
    text = msg.get("text", "")
    match = re.findall(r"!md5 (.*)", text)
    if not match: return

    return md5.md5(match[0]).hexdigest()


if __name__ == "__main__":
    import doctest; doctest.testmod()
