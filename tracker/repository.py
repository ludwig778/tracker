from pymongo import MongoClient

from tracker.settings import MONGO_CONFIG, MONGO_DATABASE, TEST

mongo_client = MongoClient(**MONGO_CONFIG)
mongo_database = getattr(mongo_client, MONGO_DATABASE)

key_collection = getattr(
    mongo_database,
    ("test_" if TEST else "") + "key"
)
measure_collection = getattr(
    mongo_database,
    ("test_" if TEST else "") + "measure"
)
