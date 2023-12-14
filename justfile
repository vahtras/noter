default:
    @just --list

list:
    python -c "import app.models; sma=app.models.SheetMusicArchive('$NOTER'); sma.table_sheets()"

import:
    python -c "import app.models; sma=app.models.SheetMusicArchive('$NOTER'); sma.save_sheets(sma.import_gss('$URL'))"
