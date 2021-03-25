import pytest

from app import crud_async

def test_create(test_app, monkeypatch):
    test_request_payload = {'email': "a@a.com", 'password': '123456AA'}
    