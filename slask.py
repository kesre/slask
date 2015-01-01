import json
import logging
import os

from flask import Flask, request

from config import config
from config import SLACK_CONF_TOKEN
from config import DATABASE_URL
from config import DEBUG

# Defaults to stdout
logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# XXX: plugins need db to run, which needs app defined.
from plugins import hooks

def run_hook(hook, data, server):
    responses = []
    for hook in hooks.get(hook, []):
        h = hook(data, server)
        if h: responses.append(h)

    return responses

def log_errors(f):
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            log.exception("Exception Caught:")
    return wrapped

@app.route("/", methods=['POST'])
@log_errors
def main():
    if DEBUG:
        log.info("Received message")
        log.info("Hooks: {0}".format(hooks))
    username = config.get("username", "slask")
    icon = config.get("icon", ":poop:")

    # ignore message we sent
    msguser = request.form.get("user_name", "").strip()
    if username == msguser or msguser.lower() == "slackbot":
        if DEBUG:
            log.info("Message was from {0} - ignored.".format(msguser))
        return ""

    # verify message actually came from slack
    token = request.form.get("token", "")
    if SLACK_CONF_TOKEN and token != SLACK_CONF_TOKEN:
        if DEBUG:
            log.info("Ignored an unverified message.")
        return ""

    text = "\n".join(run_hook("message", request.form, {"config": config, "hooks": hooks}))
    if not text:
        if DEBUG:
            log.info("No hooks acted.")
        return ""

    response = {
        "text": text,
        "username": username,
        "icon_emoji": icon,
        "parse": "full",
    }
    return json.dumps(response)

if __name__ == "__main__":
    app.run(debug=DEBUG)
