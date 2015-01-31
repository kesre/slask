"""!magic <search term> return the first magic card with name containing <search term>"""

import re
from urllib import quote

import requests

def magic(searchterm):
    searchterm = quote(searchterm)
    url = "https://api.deckbrew.com/mtg/cards?name={}"
    url = url.format(searchterm)

    j = requests.get(url).json()

    if not results:
        return "no cards found"

    card = results[0]["editions"][0]["image_url"]

    return card

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!magic (.*)", text)
    if not match: return

    searchterm = match[0]
    return magic(searchterm)
