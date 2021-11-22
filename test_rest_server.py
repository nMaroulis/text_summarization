from fastapi.testclient import TestClient

from .rest_server import app

client = TestClient(app)


def test_get_summary_by_invalid_id():

    doc_id = "abc"

    response = client.get("/text/summary/" + doc_id, headers={})
    assert response.status_code == 400


def test_get_summary():

    doc_id = 3
    response = client.get("/text/summary/"+ doc_id +"{", headers={})
    assert response.status_code == 200
    assert response.json() == {
        "document_id": 3,
        "summary": "Hi my name is Nikos",
    }



def test_get_summary_inexistent_item():
    doc_id = 100001
    response = client.get("/items/baz", headers={})
    assert response.status_code == 404
    assert response.json() == {"detail": "Document not found"}