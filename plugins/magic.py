"""!magic <search term> return magic card specified by the search term"""

import math
import re
import random
from urllib import quote

import requests

filterlist = ["type","supertype","subtype","name","oracle","set","rarity","set","color","multicolor","m","format","status"]

def search(searchterm):
    filters = getfilters(searchterm)
    if filters:
        search = reduce(lambda string, term: string + ("" if not string else "&") + "{0}={1}".format(term[0].strip(),quote(term[1].strip())), filters, "")
        url = "https://api.deckbrew.com/mtg/cards?{}".format(search)
        result = getresult(url)
    else:
        #if no filters found we default to name search
        url = "https://api.deckbrew.com/mtg/cards?name={}".format(quote(searchterm))
        results = requests.get(url).json()
        if not results:
            return "no cards found"
        #pick a random card from the matches in case we don't find a match
        result = random.choice(results)
        for card in results:
            if searchterm.lower() == card["name"].lower():
                #exact match found, pick a random edition with valid image
                result = card
                break
    
    if not result:
        return "no cards found"
    return getimage(result)

#find number of results and get a random result
def getresult(url):
    lo = 1
    hi = 2
    while requests.get(url + "&page={}".format(hi-1)).json():
        lo = hi
        hi *= 2
    while lo < hi:
        page = int(math.ceil(float(lo + hi)/float(2)))
        if requests.get(url + "&page={}".format(page-1)).json():
            lo = page
        else:
            hi = page - 1
    results = 100*(lo-1) + len(requests.get(url + "&page={}".format(lo-1)).json())
    choice = random.randint(1,results) - 1
    return requests.get(url + "&page={}".format(choice/100)).json()[choice%100]

def getfilters(searchterm):
    filters = []
    for filtertype in filterlist:
        match = re.findall(r"\+({}) ([^\+]*)".format(filtertype),searchterm)
        if match:
            for m in match:
                filters.append((m[0],m[1]))
    return filters
    
def general():
    url = "https://api.deckbrew.com/mtg/cards?supertype=legendary&type=creature"
    card = getresult(url)
    return getimage(card)

def getimage(editions):
    valideditions = [i for i in editions["editions"] if hasimage(i["image_url"])]
    if not valideditions:
        return "no image available"
    edition = random.choice(valideditions)
    return edition["image_url"]

def hasimage(url):
    return url != "https://image.deckbrew.com/mtg/multiverseid/0.jpg"

def keywordsearch(searchterm):
    generalmatch = re.findall(r"\+general", searchterm)
    if generalmatch:
        return general()
    return

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!magic ([^!]*)", text)
    if not match:
        return
    return keywordsearch(match[0]) or search(match[0])
