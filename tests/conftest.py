from pytest import fixture

from tracker.repository import key_collection, measure_collection


@fixture(autouse=True, scope="package")
def cleanup_mongo_repo():
    key_collection.drop()
    measure_collection.drop()

    yield

    key_collection.drop()
    measure_collection.drop()
