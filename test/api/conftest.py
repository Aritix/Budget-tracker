import pytest
from src.backend.app import app


@pytest.fixture()
def client():
    app.config["environment"] = "TEST"
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True, scope="function")
def set_expenses_file():
    with open('./data/test/expenses_test.saved', 'r') as savedf:
        with open('./data/test/expenses_test.yaml', 'w') as usedf:
            usedf.write(savedf.read())
    yield