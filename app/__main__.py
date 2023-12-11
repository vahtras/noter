import os
import sys

import dotenv

from .models import SheetMusic, SheetMusicArchive

dotenv.load_dotenv()
try:
    dbname = sys.argv[1]
except IndexError:
    dbname = os.environ.get('NOTER')

print(f'Connecting to {dbname=}')
sma = SheetMusicArchive(dbname)

menu = """
    Commands:
        drop [d]
        import [i]
        list [l]
        reload gss [r]
"""

try:
    while True:
        action = input(menu)
        if action[0] == 'd':
            SheetMusic.drop_collection()
        if action[0] == 'i':
            print("Importing")
            csv_file = input("csv file:")
            with open(csv_file) as f:
                sheets = sma.import_csv(f)
        if action[0] == 'l':
            sma.table_sheets()
        if action[0] == 'r':
            print()
            url = os.environ.get('URL')
            sma.import_gss(url)

except EOFError:
    print("Done")
