import os

config = {
    "username": "slaskbot",
    "icon": ":space_invader:",
}
DATABASE_URL = os.environ.get("DATABASE_URL")
DEBUG = True if os.environ.get("DEBUG") == "True" else False
SLACK_CONF_TOKEN = os.environ.get("SLACK_CONF_TOKEN")
