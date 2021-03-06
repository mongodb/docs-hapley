from api.tests.tools.setup_db import TestDatabase

test_db = TestDatabase()


# Set up local db for testing
def pytest_sessionstart():
    test_db.setup()


# Drop local db when testing is finished
def pytest_sessionfinish():
    test_db.drop_and_close()
