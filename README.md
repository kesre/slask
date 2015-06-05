﻿# Slask
### A [Slack](https://slack.com/) chatbot

## Installation

1. Clone the repo
2. `pip install -r requirements.txt`
3. Host the web app (a sample wsgi.py is included. See [here](http://flask.pocoo.org/docs/deploying/#deployment) for more on deployment)
4. Add the URL where you deployed the web app as an [outgoing webhook](https://my.slack.com/services/new/outgoing-webhook). Here's what my configuration looks like:
```
Channel: Any
Keyword(s): !, slaskbot
URL(s): https://<app_name>.herokuapp.com/
```
5. Setup config values on your environment (see config.py for os-loaded config values)
6. That's it! Try typing `!gif dubstep cat` into a chat room monitored by slask

![kitten mittens](http://i.imgur.com/xhmD6QO.png)

## Heroku

You can host for free on [Heroku](http://heroku.com). Sign up and follow the steps below to deploy the app.

```bash
heroku create
git push heroku master
heroku ps:scale web=1
heroku ps
heroku logs
```

## Commands

It's super easy to add your own commands! Just create a python file in the plugins directory with an `on_message` function that returns a string.

You can use the `!help` command to print out all available commands and a brief help message about them. `!help <plugin>` will return just the help for a particular plugin.

These are the current default plugins:

* [calc](https://github.com/llimllib/slask#calc)
* [emoji](https://github.com/llimllib/slask#emoji)
* [gif](https://github.com/llimllib/slask#gif)
* [google](https://github.com/llimllib/slask#google-or-search)
* [help](https://github.com/llimllib/slask#help)
* [image](https://github.com/llimllib/slask#image)
* [map](https://github.com/llimllib/slask#map)
* [stock](https://github.com/llimllib/slask#stock)
* [stockphoto](https://github.com/llimllib/slask#stockphoto)
* [weather](https://github.com/llimllib/slask#weather)
* [wiki](https://github.com/llimllib/slask#wiki)
* [youtube](https://github.com/llimllib/slask#youtube)

### calc

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/calc.png)

---

### emoji

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/emoji.png)

---

### flip

Different from the llimllib flip, the bot will flip / unflip text
```
 kesre: !flip me
 slaskbot (bot): (ノಠ益ಠ)ノ彡 ǝɹsǝʞ

 kesre: !unflip me
 slaskbot (bot): kesre ノ( º _ ºノ)
```
 Most text can be flipped. By default (or by specifying 'table'), a table will be flipped.

---

### gif

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/gif.png)

---

### google (or search)

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/google.png)

---

### hash

Calculate the md5 sum of passed-in text.

```
jthemphill: !md5 test
slaskbot (bot): 098f6bcd4621d373cade4e832627b4f6
```

---

### help

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/help.png)

---

### image

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/image.png)

---

### karma
Modify or view the karma of a thing. Relies on other commands
using a space after the command to avoid hook collisions.

Usage:
```
!<name>++
!<name>--
!karma <name>
!karma
```

```
 kesre: !karma chameleon
 slaskbot (bot): No karma for chameleon
 kesre: !chameleon++
 slaskbot (bot): chameleon: 1
 kesre: !karma chameleon
 slaskbot (bot): chameleon: 1
 kesre: !karma
 slaskbot (bot): Best Karma: chameleon: 1 Worst Karma:
```

---

### magic

Given a search term, returns the url for any magic cards found that match the term.

```
joshshadowfax: !magic hymn to tourach
slaskbot (bot): https://image.deckbrew.com/mtg/multiverseid/373324.jpg
```

Inline references can be used

```
joshshadowfax: Hey, check out !magic second sunrise! Good night sweet prince :D 
slaskbot (bot): https://image.deckbrew.com/mtg/multiverseid/49009.jpg
``` 

Want to do an advanced search?  Search with any of the following terms in the form +term <value>.  You can use more than one value in a search.
Valid filters:
type: Filter by specified card type (e.g. creature)
supertype: Filer by specified supertype (e.g. legendary)
subtype: Filter by specified subtype (e.g. elf)
name: Return cards which contain input in name
oracle: Return cards which contain input in oracle text
set: Return cards from specified set using 3-letter identifier (e.g. WWK)
rarity: Filter by card rarity
color: Filter by specified color
multiverseid: Find card with specified Multiverse card ID
format: Filters cards by specified format (Vintage, Legacy, Modern, Standard, Commander)
status: Filters by cards with specified status (Legal, Banned, Restricted)
multicolor: Whether to only show multicolored cards (True, False)

```
joshshadowfax: I want a card like lightning bolt.  !magic +color red +oracle 3 damage +rarity common!
slaskbot (bot): https://image.deckbrew.com/mtg/multiverseid/50292.jpg
```

Looking for a new EDH General? Use +general

```
joshshadowfax: Challenge: Build a deck with !magic +general.
slaskbot (bot): https://image.deckbrew.com/mtg/multiverseid/113512.jpg
```

---

### map

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/map.png)

---

### roll

Roll dice, displaying results.

```
!roll # rolls 1 d6
!roll 5 # rolls 5 d6
!roll d20 # rolls 1 d20
!roll 5d20 # rolls 5 d20
```

---

### stock

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/stock.png)

---

### stockphoto

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/stockphoto.png)

---

### weather

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/weather.png)

---

### wiki

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/wiki.png)

---

### youtube

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/youtube.png)

---

## Contributors

* @kesre
* @joshshadowfax
* @jthemphill

## Pre-fork Contributors

* @akatrevorjay
* @fsalum
* @llimllib
* @rodvodka
