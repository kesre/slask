"""!karma | !karma <name> | !<name>++ | !<name>-- - Modify or view karma."""
import re

from core.db import db
from models.karma import Karma

def update_karma(name, op):
    karma = db.session.query(Karma).filter_by(
        name=name
    ).with_lockmode('update').first()

    if not karma:
        karma = Karma(name)
        db.session.add(karma)

    if op == "--":
        karma.value -= 1
    elif op == "++":
        karma.value += 1
    db.session.commit()
    return str(karma)

def get_highscores():
    return db.session.query(Karma).order_by(Karma.value.desc()).limit(5).all()

def get_lowscores():
    return db.session.query(Karma).filter(
        ~Karma.id.in_([entry.id for entry in get_highscores()])
    ).order_by(Karma.value).limit(5).all()

def get_karma(text):
    if not text:
        return "Best Karma: " + ", ".join(
            [str(entry) for entry in get_highscores()]
        ) + " Worst Karma: " + ", ".join(
            [str(entry) for entry in get_lowscores()]
        )
    else:
        # If there is a word, there had to be space in front.
        name = text[1:]
        return str(
            db.session.query(Karma).filter_by(name=name).first() 
            or "No karma for {0}".format(name)
        )

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!(.*?)(\+\+|\-\-)", text)
    if match:
        return update_karma(match[0][0], match[0][1])
    
    match = re.findall(r"!karma( .+)?", text)
    if match:
        return get_karma(match[0])
    
    return ""