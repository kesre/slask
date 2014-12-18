"""!gif <search term> return a random result from the  google gif search result for <search term>"""

from urllib import quote
import re
import requests
from random import randint, choice, shuffle

def gif(searchterm_raw, unsafe=True):

    # There's a chance of pandas today
    eggs = ['panda']
    if randint(0, 100) < 10:
        searchterm_raw = '{} {}'.format(choice(eggs), searchterm_raw)

    # defaults
    opts = dict(random=10)

    # Search for opts in string
    terms = re.split(r'\b(\w+=\w+)\b', searchterm_raw)
    searchterm_raw = terms[0]
    for term in terms[1:]:
        if '=' not in term:
            continue
        opt, value = term.split('=', 1)

        if opt in ['random', 'rand', 'r']:
            if value.isdigit():
                opts['random'] = int(value)

    searchterm = quote(searchterm_raw)
    safe = "&safe="
    if not unsafe:
        safe += 'active'

    searchurl = "https://www.google.com/search?tbs=itp:animated&tbm=isch&q={0}{1}".format(searchterm, safe)
    # this is an old iphone user agent. Seems to make google return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"
    headers = {'User-agent': useragent}
    gresult = requests.get(searchurl, headers=headers).text
    gifs = re.findall(r'imgurl.*?(http.*?)\\', gresult)

    if not gifs:
        gifs = ['No images found? Quit wasting my time.']

    if opts['random']:
        gifs = gifs[:opts['random']]
        shuffle(gifs)

    # Make sure we return a valid result, only check up to a certain count
    opts['index'] = 0
    for gif in gifs[:10]:
        try:
            r = requests.get(gif, headers=headers)
            if r.ok:
                break
        except Exception:
            pass
        opts['index'] += 1

    return "{}\n{}\n{}".format(searchterm_raw, opts, gif)


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!gif (.*)", text)
    if not match:
        return
    searchterm = match[0]
    return gif(searchterm)
