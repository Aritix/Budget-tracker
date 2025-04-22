# from src.entry import Entry
from src.data_processing.entry import Entry, Entries
from src.backend.api import category
from src.backend.create_app import create_app
import json
import pytest
import os   


def test_read_category(client):
    response = client.get("/api/category")
    assert response.status_code == 200
    assert len(response.data) != 0
    categories = json.loads(response.data)
    assert type(categories) == list
    assert set(categories) == set(['Groceries', 'Rent', 'Others'])


def test_post_category(client):
    response = client.post("/api/category", json={
        "name": "Transport",
        "goal": 200
    })
    assert response.status_code == 204
    response = client.get("/api/category")
    assert len(response.data) != 0
    categories = json.loads(response.data)
    assert type(categories) == list
    assert set(categories) == set(['Groceries', 'Rent', 'Others', 'Transport'])


def test_delete_category(client):
    response = client.delete("/api/category/Groceries")
    assert response.status_code == 204
    response = client.get("/api/category")
    assert len(response.data) != 0
    categories = json.loads(response.data)
    assert type(categories) == list
    assert set(categories) == set(['Rent', 'Others'])

def test_edit_category(client):
    response = client.put("/api/category/Groceries", json={'UBER' : 'UBEREAT'})
    assert response.status_code == 204
    with open('./data/test/expenses_test.yaml', 'r') as f:
        assert f.read().count('UBEREAT') == 1
