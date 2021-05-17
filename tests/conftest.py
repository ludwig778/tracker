from pytest import fixture

from tracker.repository import mongo_repo


@fixture(autouse=True, scope="package")
def cleanup_mongo_repo():
    mongo_repo.drop("key")
    mongo_repo.drop("measure")

    yield

    mongo_repo.drop("key")
    mongo_repo.drop("measure")
