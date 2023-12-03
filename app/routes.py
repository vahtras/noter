import base64
import re

import flask

from . import app
from .forms import SearchForm
from .models import SheetMusic

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    sheets = []
    if form.validate_on_submit():
        patterns = dict()

        if form.title.data:
            patterns.update(dict(
                title=re.compile(form.title.data.strip(), re.IGNORECASE),
            ))

        if form.composer.data:
            if "," in form.composer.data:
                last, first = (_.strip() for _ in form.author.data.split(','))
            else:
                last = form.composer.data.strip()
                first = ""

            last = re.compile(last, re.IGNORECASE)
            first = re.compile(first, re.IGNORECASE)
            if first:
                composer_pattern = dict(
                    __raw__={
                        "composers": {
                            "$elemMatch": {
                                "last": last,
                                "first": first
                            }
                        }
                    }
                )
            else:
                composer_pattern = dict(
                    __raw__={"composers": { "$elemMatch": {"last": last}}}
                )

            patterns.update(composer_pattern)

        sheets = SheetMusic.objects(**patterns)
    return flask.render_template(
        'index.html', form=form, sheets=sheets, encode=base64.b64encode
    )

@app.route('/api')
def api():
    print(flask.request.args)
    filters = {k: v for k, v in flask.request.args.items() if k in ['hylla', 'title']}
    if 'last' in flask.request.args:
        filters['composers__0__last'] = flask.request.args['last']
    books = SheetMusic.objects(**filters)
    return flask.render_template('start.html', books=books, encode=base64.b64encode)
