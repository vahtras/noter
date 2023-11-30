import mongoengine
import mongomock
import mongomock.gridfs
import pytest

from app.models import SheetMusicArchive

@pytest.fixture(scope='session')
def connection():
    # see https://github.com/mongomock/mongomock/issues/639
    mongomock.gridfs.enable_gridfs_integration()
    connection = mongoengine.connect(
        'pytest',
        mongo_client_class=mongomock.MongoClient,
        alias='default'
    )
    yield connection
    mongoengine.disconnect()

@pytest.fixture
def sma(connection):
    sma = SheetMusicArchive()
    sma.connection = connection
    yield sma
