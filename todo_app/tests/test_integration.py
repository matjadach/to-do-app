import pytest, requests, os
from dotenv import load_dotenv, find_dotenv
from todo_app import app

@pytest.fixture
def client():
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

class StubResponse(): 
    def __init__(self, fake_response_data): 
        self.fake_response_data = fake_response_data 

    def json(self): 
        return self.fake_response_data         

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', get_lists_stub)
    response = client.get("/")

    assert response.status_code == 200

def get_lists_stub(method, url, headers = {}): 
    test_api_key = os.environ.get('API_KEY')
    test_api_token = os.environ.get('API_TOKEN') 
    test_inprogress_list = os.environ.get('INPROGRESS_LIST')
    test_notstarted_list = os.environ.get('NOTSTARTED_LIST')
    test_done_list = os.environ.get('COMPLETED_LIST')
    fake_response_data = None
    if url == f'https://api.trello.com/1/lists/{test_inprogress_list}?key={test_api_key}&token={test_api_token}': 
        fake_response_data = { 
            'id': '123abc', 
            'name': 'To Do', 
            'cards': [{'id': '456', 'name': 'Test card'}] 
        }
    elif url == f'https://api.trello.com/1/lists/{test_notstarted_list}?key={test_api_key}&token={test_api_token}': 
        fake_response_data = { 
            'id': '123abc', 
            'name': 'Not started', 
            'cards': [{'id': '456', 'name': 'Test card'}] 
        }
    elif url == f'https://api.trello.com/1/lists/{test_done_list}?key={test_api_key}&token={test_api_token}': 
        fake_response_data = { 
            'id': '123abc', 
            'name': 'Not started', 
            'cards': [{'id': '456', 'name': 'Test card'}] 
        }
    elif url == f'https://api.trello.com/1/lists/{test_inprogress_list}/cards?key={test_api_key}&token={test_api_token}':
        fake_response_data = [
            {
        "id": "61fbb76b4a2b2a69f9e593bb",
        "dateLastActivity": "2022-02-03T11:09:36.676Z",
        "desc": "app",
        "name": "Another to do",
        "due": "2022-02-03T00:00:00.000Z",
            }]
    elif url == f'https://api.trello.com/1/lists/{test_notstarted_list}/cards?key={test_api_key}&token={test_api_token}':
        fake_response_data = [
            {
        "id": "61fbb76b4a2b2a69f9e593bb",
        "dateLastActivity": "2022-02-03T11:09:36.676Z",
        "desc": "app",
        "name": "Another to do",
        "due": "2022-02-03T00:00:00.000Z",
            }]
    elif url == f'https://api.trello.com/1/lists/{test_done_list}/cards?key={test_api_key}&token={test_api_token}':
        fake_response_data = [
            {
        "id": "61fbb76b4a2b2a69f9e593bb",
        "dateLastActivity": "2022-02-03T11:09:36.676Z",
        "desc": "app",
        "name": "Another to do",
        "due": "2022-02-03T00:00:00.000Z",
            }]

    return StubResponse(fake_response_data)

def test_add_task(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', add_task_stub)
    response = client.post('/add', data={
        "title": "testtitle",
        "desc": "testdesc",
        "dueby": "2022-02-01T00:00:00.000Z"
    })

    assert response.status_code == 302 #redirect to home page

def add_task_stub(method, url, headers):
    test_api_key = os.environ.get('API_KEY')
    test_api_token = os.environ.get('API_TOKEN')
    test_list = os.environ.get('NOTSTARTED_LIST')
    fake_response_data = None
    title = 'Testing'
    desc = 'Testing'
    dueby = '2022-02-01T00:00:00.000Z'
    if url == f'https://api.trello.com/1/lists/{test_list}/cards?key={test_api_key}&token={test_api_token}&name={title}&desc={desc}&dueby={dueby}':
        fake_response_data = [{
            'id': '124125125215',
            'cards': [{'id': '456', 'name': 'Test card'}] 
        }]
    return StubResponse(fake_response_data)

