"""!magic <search term> return the first magic card with name containing <search term>"""

import re
import random
from urllib import quote

import requests

def magic(searchterm):
    quotedsearchterm = quote(searchterm)
    url = "https://api.deckbrew.com/mtg/cards?name={}"
    url = url.format(quotedsearchterm)

    results = requests.get(url).json()

    if not results:
        return "no cards found"

    for card in results:
        if searchterm.lower() == card["name"].lower():
            #exact match found, pick a random edition with valid image
            return getimage(card)
        
    #no exact match found, pick a random card from the matches
    card = random.choice(results)
    return getimage(card)

def getimage(editions):
    valideditions = [i for i in editions["editions"] if hasimage(i["image_url"])]
    if not valideditions:
        return "no image available"
    edition = random.choice(valideditions)
    return edition["image_url"]

def hasimage(url):
    return url != "https://image.deckbrew.com/mtg/multiverseid/0.jpg"

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!magic ([^!]*)", text)
    if not match: return

    searchterm = match[0]
    return magic(searchterm)
