"""!amazing will return an image of the LoL player Amazing"""
import re
import requests

amazing = "http://40.media.tumblr.com/a8b7e3e986ca53e909cb948dbad38ae6/tumblr_ndatdp0Jrb1tjmq8fo1_1280.jpg"

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!amazing", text)
    if not match: return

    return amazing
