import json
from pathlib import Path

from pymongo import InsertOne, MongoClient

TEST_LOCAL_DB_URI = "mongodb://localhost:27017"
TEST_DB_NAME = "hapley_test"
COLL_ENTITLEMENTS = "entitlements"
COLL_REPOS_BRANCHES = "repos_branches"


class TestDatabase:
    def __init__(self):
        self.client = MongoClient(TEST_LOCAL_DB_URI)

    def _bulk_insert_items(self, collection, filename):
        base_path = Path(__file__).parent
        file_path: Path = base_path / filename

        with file_path.resolve().open("r") as f:
            data = json.load(f)
            writes = [InsertOne(item) for item in data]

        collection.bulk_write(writes)

    # Reminder: Ensure that local database is set up and running first
    # TODO: Set up indexes for each collection.
    def setup(self):
        print("Setting up local database for testing")

        client = self.client

        if TEST_DB_NAME in self.client.list_database_names():
            client.drop_database(TEST_DB_NAME)

        db = client[TEST_DB_NAME]
        entitlements_coll = db[COLL_ENTITLEMENTS]
        repos_coll = db[COLL_REPOS_BRANCHES]

        relative_path_to_test_data = "../data"
        self._bulk_insert_items(
            entitlements_coll, f"{relative_path_to_test_data}/entitlements.json"
        )
        self._bulk_insert_items(
            repos_coll, f"{relative_path_to_test_data}/repos_branches.json"
        )

        print("Finished setting up local database for testing")

    def drop_and_close(self):
        print("\n\nDropping local database used for testing")

        client = self.client

        if TEST_DB_NAME in client.list_database_names():
            client.drop_database(TEST_DB_NAME)

        client.close()
        print("Finished removing database for testing")
