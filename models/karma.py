from core.citext import CIText
from core.db import db

class Karma(db.Model):

    __hash__ = None
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(CIText(), unique=True)
    value = db.Column(db.Integer())

    def __init__(self, name):
        self.name = name
        self.value = 0

    def __repr__(self):
        return self.name + ': ' + str(self.value)

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value and self.name == other.name

    def __ne__(self, other):
        return not self == other
