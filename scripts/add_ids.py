"""
    DOP-3157: Add unique IDs to elements in document arrays
    Author: Drew Beckmen
"""

from pymongo import MongoClient, collection
from bson import ObjectId
from decouple import config
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-env', '--environment', choices=['dev', 'test', 'prod'], help='Environment to run the script in', default='dev')
parser.add_argument('--rollback', action='store_true', help="Drop email address field from collection")
args = parser.parse_args()

COLLECTION_NAME_BY_ENVIRONMENT = {
    'dev': 'drew_repo_branches',
    'test': 'repos_branches',
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
    return MongoClient(CONNECTION_STRING, uuidRepresentation='standard')


def modify_uuids(collection: collection.Collection, removeIds: bool = False):
    print("Rollback flag not set. Adding ids to subdocuments in branches and groups fields")
    for doc in collection.find():
        for branch in doc['branches']:
            if removeIds:
                del branch['id']
            else:
              branch['id'] = ObjectId()
        groups = 'groups' in doc and doc['groups']
        if groups:
            for group in groups:
                if removeIds:
                    del group['id']
                else:
                  group['id'] = ObjectId()
        collection.update_one({'_id': doc['_id']}, {'$set': doc})
    print(f"Finished {'removing' if removeIds else 'adding'} ids to documents.")

def execute() -> bool:
    db = connect().get_database(DATABASE_BY_ENVIRONMENT[args.environment])
    collection = db.get_collection(COLLECTION_NAME_BY_ENVIRONMENT[args.environment])
    print(f"Connected to {DATABASE_BY_ENVIRONMENT[args.environment]}.{COLLECTION_NAME_BY_ENVIRONMENT[args.environment]}")

    if args.rollback:
        modify_uuids(collection, removeIds=True)
    else:
        modify_uuids(collection)

    return True

if __name__ == '__main__':
    print(f'Starting... Running in {args.environment} environment')
    execute() and print('Done.')