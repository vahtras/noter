#!/usr/bin/env python
import os

import dotenv
import flask
import mongoengine

from config import Config

dotenv.load_dotenv()
dbname = os.environ.get('NOTER')
mongoengine.register_connection(alias='default', name=dbname)

app = flask.Flask(__name__)
app.config.from_object(Config)

from . import routes # noqa: F401 E402 # to avoid circular import

if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get("PORT", 5000))
