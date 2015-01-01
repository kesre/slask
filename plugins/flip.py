# -*- coding: utf-8 -*-
"""!flip [<text>] - flip text or table.
Based on https://github.com/github/hubot-scripts/blob/master/src/scripts/flip.coffee
Similar license
"""
import re

from upsidedown import transform

TABLES = [" table", " a table", " the table"]

def replace_me_with_user(text, user_name):
    if text == " me":
       return user_name
    return text

def flip(to_flip):
    if not to_flip or to_flip in TABLES:
        flipped = u"┻━┻"
    else:
        flipped = transform(to_flip)
    return u"(ノಠ益ಠ)ノ彡 " + flipped

def unflip(text):
    if not text or text in TABLES:
        text = u"┬──┬"
    return text + u" ノ( º _ ºノ)"

def on_message(msg, server):
    text = msg.get("text", "")
    user_name = msg.get("user_name", "")
    match = re.findall(r"!flip( .*)?", text)
    if match:
        return flip(replace_me_with_user(match[0], user_name))

    match = re.findall(r"!(unflip|putback)( .*)?", text)
    if match:
        return unflip(replace_me_with_user(match[0][1], user_name))

    return ""