import csv

import pandas as pd
import rich.table
import rich.console

from mongoengine import (
    register_connection,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FileField,
    IntField,
    ListField,
    StringField,
    ValidationError
)

TRANSLATIONS = {
    'Titel': 'title',
    'År': 'year',
    'Tonsättare': 'composers',
    'Text': 'lyrics',
    'Arr': 'arrangement',
    'Besättning': 'parts',
    'Solist': 'soloist',
    'Instrument': 'instruments',
    'Språk': 'language',
    'Placering': 'location',
}


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
    year = IntField()
    composers = ListField(EmbeddedDocumentField(Composer))
    lyrics = StringField(default="")
    arrangement = StringField(default="")
    parts = StringField()
    soloist = StringField()
    instruments = StringField()
    language = StringField()
    location = StringField(default="")
    pdf = FileField()
    row_id = IntField()
    meta = {'collection': 'noter'}

    def __repr__(self):
        return f'SheetMusic(title="{self.title}")'

    def __str__(self):
        return f'{self.title}'

class SheetMusicArchive:

    def __init__(self, dbname='default'):
        self.dbname = dbname
        self.connect()

    def __repr__(self):
        return self.dbname

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

    def import_gss(self, url: str) -> list[SheetMusic]:
        """
        Read Google spreadsheet to list of SheetMusic objects for further
        processing
        """
        df = pd.read_csv(url)
        df.columns = [TRANSLATIONS[h]for h in df.columns]

        new_sheets = []
        for row, rec in df.iterrows():
            rec = rec.dropna()
            rec['composers'] = [Composer.from_comma_string(rec['composers'])]
            rec['row_id'] = row + 2
            try:
                new_sheets.append(
                    SheetMusic(**rec)
                )
            except KeyError as ke:
                print(ke)
                print(rec)
                breakpoint()

        return new_sheets

    def save_sheets(self, new_sheets: list[SheetMusic]) -> None:
        """
        Save modified sheets to db
        """
        for sm in new_sheets:
            if SheetMusic.objects(title=sm.title):
                print(f'{sm} exists')
            else:
                print(f'{sm} added')
                try:
                    sm.save()
                except ValidationError as ve:
                    print(ve)
                    breakpoint()

    def delete_sheets(self, **pattern):
        for sheet in SheetMusic.objects(**pattern):
            sheet.delete()

    def table_sheets(self, **pattern):
        table = rich.table.Table()
        table.add_column(' 1')
        table.add_column('Titel')
        table.add_column('År')
        table.add_column('Tonsättare')
        table.add_column('Text')
        table.add_column('Arr')
        table.add_column('Besättning')
        table.add_column('Soloist')
        table.add_column('Instrument')
        table.add_column('Språk')
        table.add_column('Placering')
        for sheet in SheetMusic.objects(**pattern):
            table.add_row(
                f'{sheet.row_id:2d}',
                sheet.title,
                str(sheet.year) if sheet.year else "",
                sheet.composers[0].last + ", " + sheet.composers[0].first,
                sheet.lyrics,
                sheet.arrangement,
                sheet.parts,
                sheet.soloist,
                sheet.instruments,
                sheet.language,
                sheet.location,
            )
        console = rich.console.Console()
        console.print(table)
