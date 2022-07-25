import json
from pathlib import Path

from pymongo import InsertOne, MongoClient

LOCAL_URI = "mongodb://localhost:27017"
DB_NAME = "hapley_test"
COLL_ENTITLEMENTS = "entitlements"
COLL_REPOS_BRANCHES = "repos_branches"


def bulk_insert_items(collection, filename):
    writes = []

    base_path = Path(__file__).parent
    file_path = base_path / filename
    f = open(file_path)

    data = json.load(f)
    for item in data:
        writes.append(InsertOne(item))

    result = collection.bulk_write(writes)
    print(result.bulk_api_result)


# Reminder: Ensure that local database is set up and running first
# TODO: Set up indexes for each collection.
def setup_test_db():
    print("Setting up local database for testing")

    client = MongoClient(LOCAL_URI)

    if DB_NAME in client.list_database_names():
        client.drop_database(DB_NAME)

    db = client[DB_NAME]
    entitlements_coll = db[COLL_ENTITLEMENTS]
    repos_coll = db[COLL_REPOS_BRANCHES]

    bulk_insert_items(entitlements_coll, "./data/entitlements.json")
    bulk_insert_items(repos_coll, "./data/repos_branches.json")

    client.close()

    print("Finished setting up local database for testing")


def drop_test_db():
    print("\nDropping local database used for testing")
    client = MongoClient(LOCAL_URI)

    if DB_NAME in client.list_database_names():
        client.drop_database(DB_NAME)

    client.close()
    print("Finished removing database for testing")
