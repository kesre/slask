import json
import logging
import os

from flask import Flask, request

from config import config
from config import SLACK_CONF_TOKENS
from config import CHANNEL_MOD_MAP
from config import CHANNEL_MOD_OPT_IN
from config import DATABASE_URL
from config import DEBUG
import constants

# Defaults to stdout
logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# XXX: plugins need db to run, which needs app defined.
from plugins import hooks

def run_hooks(protocol, data, server):
    responses = []
    protocol_hooks = hooks.get(protocol, [])
    for hook in get_channel_hooks(protocol_hooks, server["channel"]):
        h = hook(data, server)
        if h: responses.append(h)

    return responses

def get_channel_hooks(hooks, channel):
    """Because not everyone wants ALL the hooks ALL the time."""
    if channel in CHANNEL_MOD_MAP:
        mods = CHANNEL_MOD_MAP[channel]
        if mods == constants.CHANNEL_MOD_ALL:
            return hooks.itervalues()
        return [hooks[mod] for mod in mods]
    return hooks.itervalues() if not CHANNEL_MOD_OPT_IN else []

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
        log.info("Hooks: {0}".format(hooks.keys()))
    username = config.get("username", constants.DEFAULT_BOT_NAME)
    icon = config.get("icon", constants.DEFAULT_BOT_ICON)

    # ignore message we sent
    msguser = request.form.get("user_name", "").strip()
    if username == msguser or msguser.lower() == constants.SLACKBOT_NAME:
        if DEBUG:
            log.info("Message was from {0} - ignored.".format(msguser))
        return ""

    # verify message actually came from slack
    token = request.form.get("token", "")
    if SLACK_CONF_TOKENS and token not in SLACK_CONF_TOKENS:
        log.info("Ignored an unverified message.")
        return ""

    channel = request.form.get("channel_name", "")
    text = "\n".join(run_hooks("message", request.form, {"config": config, "hooks": hooks, "channel": channel}))
    if not text:
        log.info("No hooks acted.")
        return ""

    if request.form.get("command"):
        response = text
    else:
        response = {
            "text": text,
            "username": username,
            "icon_emoji": icon,
            "parse": "full",
        }
    return json.dumps(response)

if __name__ == "__main__":
    app.run(debug=DEBUG)
