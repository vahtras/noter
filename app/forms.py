from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    title = StringField('Titel', validators=[])
    composer = StringField('Tonsättare', validators=[])
    parts = StringField('Besättning', validators=[])
    soloist = StringField('Solist', validators=[])
    language = StringField('Språk', validators=[])
    submit = SubmitField()
