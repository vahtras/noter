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

    def __str__(self):
        return f"{self.last}, {self.first}"

    @staticmethod
    def from_comma_string(cstr):
        if ',' in cstr:
            last, first = cstr.split(',')
        else:
            last = cstr
            first = ""
        return Composer(last=last.strip(), first=first.strip())

class SheetMusic(Document):
    title = StringField(required=True)
    composers = ListField(EmbeddedDocumentField(Composer))
    parts = StringField()
    soloist = StringField()
    instruments = StringField()
    language = StringField()
    location = StringField()
    meta = {'collection': 'noter'}

    def __repr__(self):
        return f'SheetMusic(title="{self.title}")'

    def __str__(self):
        return f'{self.title}'

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
         try:
            new_sheets.append(
                SheetMusic(
                    title=rec["Titel"],
                    composers=[Composer.from_comma_string(rec["Tonsättare"])],
                    parts=rec["Besättning"],
                    soloist=rec["Solist"],
                    instruments=rec["Instrument"],
                    language=rec["Språk"],
                )
            )
         except KeyError:
             breakpoint()

        for sm in new_sheets:
            sm.save()

        return new_sheets
