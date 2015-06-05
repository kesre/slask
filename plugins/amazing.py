"""!amazing will return an image of the LoL player Amazing"""
import re
import requests

amazing = "http://www.tsm.gg/wp-content/uploads/2014/07/amazing-200x200.jpg"

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!amazing", text)
    if not match: return

    return amazing
