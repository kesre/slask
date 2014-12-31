from glob import glob
import importlib
import json
import logging
import os
import re
import sys
import traceback

from flask import Flask, request
app = Flask(__name__)

curdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curdir)

from config import config
from config import SLACK_CONF_TOKEN

# Defaults to stdout
logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

hooks = {}
def init_plugins():
    for plugin in glob('plugins/[!_]*.py'):
        print "plugin: %s" % plugin
        try:
            mod = importlib.import_module(plugin.replace(os.path.sep, ".")[:-3])
            modname = mod.__name__.split('.')[1]
            for hook in re.findall("on_(\w+)", " ".join(dir(mod))):
                hookfun = getattr(mod, "on_" + hook)
                print "attaching %s.%s to %s" % (modname, hookfun, hook)
                hooks.setdefault(hook, []).append(hookfun)

            if mod.__doc__:
                firstline = mod.__doc__.split('\n')[0]
                hooks.setdefault('help', {})[modname] = firstline
                hooks.setdefault('extendedhelp', {})[modname] = mod.__doc__

        #bare except, because the modules could raise any number of errors
        #on import, and we want them not to kill our server
        except:
            print "import failed on module %s, module not loaded" % plugin
            print "%s" % sys.exc_info()[0]
            print "%s" % traceback.format_exc()

init_plugins()

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
            log.exception()
    return wrapped

@app.route("/", methods=['POST'])
@log_errors
def main():
    username = config.get("username", "slask")
    icon = config.get("icon", ":poop:")

    # ignore message we sent
    msguser = request.form.get("user_name", "").strip()
    if username == msguser or msguser.lower() == "slackbot":
        return ""

    # verify message actually came from slack
    token = request.form.get("token", "")
    if SLACK_CONF_TOKEN and token != SLACK_CONF_TOKEN:
        return ""

    text = "\n".join(run_hook("message", request.form, {"config": config, "hooks": hooks}))
    if not text:
        return ""

    response = {
        "text": text,
        "username": username,
        "icon_emoji": icon,
        "parse": "full",
    }
    return json.dumps(response)

if __name__ == "__main__":
    app.run(debug=True)
