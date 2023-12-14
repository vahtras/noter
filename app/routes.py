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
                last, first = (_.strip() for _ in form.composer.data.split(','))
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

        if form.parts.data:
            parts_pattern = re.compile(form.parts.data.strip(), re.IGNORECASE)
            patterns.update({'parts': parts_pattern})

        if form.language.data:
            language_pattern = re.compile(form.language.data.strip(), re.IGNORECASE)
            patterns.update({'language': language_pattern})

        sheets = SheetMusic.objects(**patterns)
    return flask.render_template(
        'index.html', form=form, sheets=sheets, encode=base64.b64encode
    )

@app.route('/api')
def api():
    print(flask.request.args)
    filters = {
        k: v
        for k, v in flask.request.args.items()
        if k in ['title', 'year', 'parts']
    }
    if 'last' in flask.request.args:
        filters['composers__0__last'] = flask.request.args['last']
    sheets = SheetMusic.objects(**filters)
    return flask.render_template('start.html', sheets=sheets, encode=base64.b64encode)


@app.route('/rad/<row_id>')
def row(row_id: int):
    sheet = SheetMusic.objects(row_id=row_id).first()
    return flask.render_template('sheet.html', sheet=sheet)
