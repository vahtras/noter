default:
    @just --list

list:
    python -c "from app.models import SheetMusicArchive as notbib; notbib('vahtras').table_sheets()"
