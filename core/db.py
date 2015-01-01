from flask.ext.sqlalchemy import SQLAlchemy

import slask

db = SQLAlchemy(slask.app)