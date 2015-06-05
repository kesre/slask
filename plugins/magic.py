"""!magic <search term> return magic card specified by the search term"""

import math
import re
import random
from urllib import quote

import requests

class Filter:
    def __init__(self, term, value=None):
        self.term = term
        self.value = value
    def setvalue(self, value):
        self.value = value

class BasicFilter(Filter):
    def printfilter(self):
        return "{0}={1}".format(self.term, quote(self.value))
class AliasFilter(Filter):
    def printfilter(self):
        return self.value
    #For AliasFilters, there's no value to set since the alias is constant
    def setvalue(self,value):
        return
    

filterlist = [BasicFilter("type"),BasicFilter("supertype"),BasicFilter("subtype"),BasicFilter("name"),
              BasicFilter("oracle"),BasicFilter("set"),BasicFilter("rarity"),BasicFilter("set"),BasicFilter("color"),
              BasicFilter("multicolor"),BasicFilter("multiverseid"),BasicFilter("format"),BasicFilter("status"),
              AliasFilter("general", "supertype=legendary&type=creature")]

imagehandler = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={}&type=card"

#number of items max returned on a page.
items = 100

def search(searchterm):
    filters = getfilters(searchterm)
    result = None
    results = 0
    hasname = False

    if filters:
        search =  "&".join([i.printfilter() for i in filters])
        url = "https://api.deckbrew.com/mtg/cards?{}".format(search)
        for f in filters:
            if f.term.lower() == "name":
                hasname = True
                break
        results = getnumresults(url)
    else:
        #if no filters found we default to name search
        url = "https://api.deckbrew.com/mtg/cards?name={}".format(quote(searchterm))
        hasname = True
        results = getnumresults(url)

    if results == 0:
        return "no cards found"
    
    #if name filter was used, try to find an exact match first
    if hasname:
        term = searchterm
        for f in filters:
            if f.term.lower() == "name":
                term = f.value
                break
        for i in range(0, results/items + 1):
            cards = requests.get(url + "&page={}".format(i)).json()
            for card in cards:
                if term.lower() == card["name"].lower():
                    result = card
                    break
            if result:
                break
    if not result:
        #no exact match found, get random result instead
        result = getrandomresult(url, results)
    
    if not result:
        return "no cards found"
    return getimage(result)

#find number of results
def getnumresults(url):
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
    return items*(lo-1) + len(requests.get(url + "&page={}".format(lo-1)).json())

def getrandomresult(url, numresults):
    choice = random.randint(1,numresults) - 1
    return requests.get(url + "&page={}".format(choice/items)).json()[choice%items]

def getfilters(searchterm):
    filters = []
    for f in filterlist:
        match = re.findall(r"\+({})([^\+]*)".format(f.term),searchterm)
        if match:
            for m in match:
                f.setvalue(m[1].strip())
                filters.append(f)
    return filters

def getimage(editions):
    valideditions = [i for i in editions["editions"] if i["multiverse_id"]]
    if not valideditions:
        return "no image available"
    edition = random.choice(valideditions)
    return imagehandler.format(edition["multiverse_id"])

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!magic ([^!]*)", text)
    if not match:
        return
    return search(match[0])
