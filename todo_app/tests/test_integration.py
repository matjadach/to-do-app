import mongomock
import pymongo
import pytest
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from todo_app import app


@pytest.fixture
def client():
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=('mongodb://fakemongo.com:27017')):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    fake_object = {
        "_id": "100",
        "title": "fake title",
        "desc": "fake desc",
        "status": "In progress",
        "due": "2022-02-03T00:00:00.000Z",
        "last_modified": (datetime.now()).isoformat()
    }

    mongo_client = pymongo.MongoClient('mongodb://fakemongo.com:27017')
    mongo_client.fake_db.fake_todo_collection.insert_one(fake_object)

    response = client.get('/')
    assert response.status_code == 200 #Not entirely sure this test works as it should. Also it would be great to test other functionality... to do I guess
