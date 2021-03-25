from fastapi import status
from starlette.status import HTTP_200_OK


def test_root(test_app):
    response = test_app.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Welcome to PockiLand Network API server :)"}
