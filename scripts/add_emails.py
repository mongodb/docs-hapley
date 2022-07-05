"""
    DOP-3103: Add email address to every user
    Author: Drew Beckmen

    The goal of this ticket is to add a populated email address
    field to each document in the entitlements collection in the pool database.
    We use a Realm endpoint from Mana to find the email address for each user.
"""

from pymongo import MongoClient, collection
from typing import Optional
from decouple import config
import argparse
import requests as r

parser = argparse.ArgumentParser()
parser.add_argument('-env', '--environment', choices=['dev', 'test', 'prod'], help='Environment to run the script in', default='dev')
parser.add_argument('--rollback', action='store_true', help="Drop email address field from collection")
args = parser.parse_args()

COLLECTION_NAME_BY_ENVIRONMENT = {
    'dev': 'drew_entitlements_dev',
    'test': 'entitlements',
    'prod': 'entitlements'
} 

DATABASE_BY_ENVIRONMENT = {
    'dev': 'pool_test',
    'test': 'pool_test',
    'prod': 'pool'
}


def connect() -> MongoClient:
    DB_USERNAME = config('DB_USERNAME')
    DB_PASSWORD = config('DB_PASSWORD')
    CONNECTION_STRING = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.ylwlz.mongodb.net/snooty_dev"
    return MongoClient(CONNECTION_STRING)

# Queries Realm endpoint for user email address
def find_email(github_username: str) -> Optional[str]:
    base_url = "https://webhooks.mongodb-realm.com/api/client/v2.0/app/clouddevgithub-blcki/service/http/incoming_webhook/github"
    json_payload = {
        'github': github_username
    }
    headers = {
        'Api-Key': config('REALM_API_KEY')
    }
    response = r.post(base_url, json=json_payload, headers=headers)
    if response.status_code == 200:
        return response.json()['uid']
    else:
        return None


def remove_emails(collection: collection.Collection):
    print("Rollback flag set. Removing email address field from documents")
    collection.update_many({}, {'$unset': {'email': 1}})
    print("Dropped email address field from collection")


def set_emails(collection: collection.Collection):
    print("Rollback flag not set. Adding email address field to documents")
    numErrors = 0
    numSuccess = 0
    for doc in collection.find():
        email = find_email(doc['github_username'])
        if email:
            doc['email'] = email
            collection.replace_one({'_id': doc['_id']}, doc)
            numSuccess += 1
        else:
            print(f"Received non-200 status code for {doc['github_username']}")
            numErrors += 1
    print(f"Finished adding email address to documents. Encountered {numErrors} errors, {numSuccess} successes")

def execute() -> bool:
    db = connect().get_database(DATABASE_BY_ENVIRONMENT[args.environment])
    collection = db.get_collection(COLLECTION_NAME_BY_ENVIRONMENT[args.environment])
    print(f"Connected to {DATABASE_BY_ENVIRONMENT[args.environment]}.{COLLECTION_NAME_BY_ENVIRONMENT[args.environment]}")

    if args.rollback:
        remove_emails(collection)
    else:
        set_emails(collection)

    return True

if __name__ == '__main__':
    print(f'Starting... Running in {args.environment} environment')
    execute() and print('Done.')
