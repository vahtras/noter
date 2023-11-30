import csv

from mongoengine import (
    register_connection,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    ListField,
    StringField,
)


class Composer(EmbeddedDocument):
    last = StringField(required=True)
    first = StringField()
    years = ListField(IntField())
    meta = {'collection': 'composers'}

    @staticmethod
    def from_comma_string(cstr):
        last, first = cstr.split(',')
        return Composer(last=last.strip(), first=first.strip())

class SheetMusic(Document):
    title = StringField(required=True)
    composers = ListField(EmbeddedDocumentField(Composer))
    parts = StringField()
    soloist = StringField()
    instruments = StringField()
    language = StringField()
    location = StringField()

    def __repr__(self):
        return f'SheetMusic(title="{self.title}")'

class SheetMusicArchive:

        def __init__(self, dbname=None):
            self.dbname = dbname
            self.connect()

        def __repr__(self):
            self.dbname

        def connect(self):
            self.connection = register_connection(
                alias='default',
                name=self.dbname,
            )

        def import_csv(
            self, csv_stream=None, field_separator: str = ","
        ) -> list[SheetMusic]:
            new_sheets = []
            for rec in csv.DictReader(csv_stream, delimiter=field_separator):
                new_sheets.append(
                    SheetMusic(
                        title=rec["Titel"],
                        composers=[Composer(last=rec["Tonsättare"])],
                        parts=rec["Besättning"],
                        soloist=rec["Solist"],
                        instruments=rec["Instrument"],
                        language=rec["Språk"],
                    )
                )
            return new_sheets
