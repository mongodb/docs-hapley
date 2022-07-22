from tools.test_db import drop_test_db, setup_test_db


# Set up local db for testing
def pytest_sessionstart():
    setup_test_db()


# Drop local db when testing is finisheds
def pytest_sessionfinish():
    drop_test_db()
