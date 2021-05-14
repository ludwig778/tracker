from pytest import mark, raises

from tracker.models import Key, Measure


@mark.parametrize("kwargs", [
    {"key": "tests.key1"},
    {"key": "tests.key2"},
    {"key": "tests.key3"},
    {"key": "lmaoooo.key3"},
])
def test_create_keys(kwargs):
    assert Key.create(**kwargs)


def test_create_key_exception():
    with raises(AssertionError, match="Key must be set"):
        Key.create(key=None)


def test_list_prefix_keys():
    assert len(Key.list_prefix("lmao")) == 1
    assert len(Key.list_prefix("tests")) == 3


def test_list_keys():
    assert len(Key.list()) == 4


def test_get_key():
    assert Key.get("tests.key1")


def test_get_non_existing_key():
    assert Key.get("non_existing") is None


def test_delete_key():
    Key.get("lmaoooo.key3").delete()

    assert len(Key.list()) == 3


def test_update_key():
    key = Key.get("tests.key3")
    key.update(description="Test description", key="tests.key4")

    assert Key.get("tests.key4")


@mark.parametrize("kwargs", [
    {"key": "tests.key1", "value": 23.3, "timestamp": 123},
    {"key": "tests.key1", "value": 23.7, "timestamp": 125},
    {"key": "tests.key1", "value": 24, "timestamp": 127},
    {"key": "tests.key2", "value": 123, "timestamp": 1234},
])
def test_create_measures(kwargs):
    assert Measure.create(**kwargs)


@mark.parametrize("kwargs,exception_str", [
    ({}, "Key must be set"),
    ({"key": "test"}, "Value must be set"),
    ({"key": "test", "value": 23}, "Timestamp must be set"),
])
def test_create_measure_exception(kwargs, exception_str):
    with raises(AssertionError, match=exception_str):
        Measure.create(**kwargs)


def test_key_measures_property():
    assert len(Key.get("tests.key1").measures) == 3


def test_list_measures():
    assert len(Measure.list()) == 4


def test_get_last_measure():
    measure = Measure.get("tests.key1")

    assert measure.value == 24
    assert measure.timestamp == 127


def test_get_measure():
    assert Measure.get("tests.key1", timestamp=123)


def test_get_non_existing_measure():
    assert Measure.get("tests.key1", timestamp=124) is None


def test_delete_measure():
    Measure.get("tests.key1", timestamp=127).delete()

    assert len(Key.get("tests.key1").measures) == 2


def test_update_measure():
    measure = Measure.get("tests.key1", timestamp=125)
    old_value = measure.value

    measure.update(value=25)

    assert old_value != measure.value
