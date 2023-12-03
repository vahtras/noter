default:
    @just --list

list:
    python -c "from app.models import SheetMusic; SheetMusic.list_sheets()"
