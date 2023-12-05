import io
from unittest.mock import patch

import pandas as pd

from app.models import SheetMusic, Composer

def test_create_sheet_with_title():
    sheet = SheetMusic(title="Legendaarne")
    assert sheet.title == "Legendaarne"

def test_repr():
    sheet = SheetMusic(title="Legendaarne")
    assert repr(sheet) == 'SheetMusic(title="Legendaarne")'


def test_create_composer():
    composer = Composer(first="Peeter", last="Konovalov", years=(1962,))
    assert composer.first == "Peeter"
    assert composer.last == "Konovalov"
    assert composer.years == [1962,]

def test_composer_from_comma_field():
    full = "Last, First"
    composer = Composer.from_comma_string(full)
    assert composer.first == 'First'
    assert composer.last == 'Last'

def test_create_book_with_one_author():
    sheet = SheetMusic(
        title="Legendaarne",
        composers=[
            Composer(
                last="Konovalov",
                first="Peeter",
                years=(1962,)
            )
        ]
    )
    assert sheet.title == "Legendaarne"

def test_sheet_to_db(mongodb, sma):
    sheet = SheetMusic(title="Magnificat",
        composers=[Composer(first="Arvo", last="Pärt")]
    )
    sheet.save()

    new = SheetMusic.objects().first()
    assert new.title == "Magnificat"

def test_sheet_location():
    SheetMusic(title="Magnificat", location="Folder").save()
    search = SheetMusic.objects(location="Folder").first()
    assert search.title == "Magnificat"


def test_import_csv_new(sma):
    finp = io.StringIO(
"""Titel,Tonsättare,Besättning,Solist,Instrument,Språk
Magnificat,Pärt,SSATB,S,,Latin
"""
    )
    with patch('app.models.input') as mock_input:
        mock_input.side_effect = ["y", EOFError]
        sheets = sma.import_csv(finp)

    assert sheets[0].title == "Magnificat"

def test_import_gss(sma):
    gdoc = (
        'https://docs.google.com/spreadsheets/d/'
        '1D4UoThfcQSELBqfAomB9UY-SGzAEsHMYEEg270D-b18/'
        'export?format=csv'
    )
    sheets = sma.import_gss(gdoc)
    assert sheets[0].title == 'Magnificat'

