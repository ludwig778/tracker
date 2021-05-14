from tracker.repository.mongo import key_collection, measure_collection


class Key:
    def __init__(self, key=None, _id=None, description=None):
        self.id = _id
        self.key = key
        self.description = description

    @classmethod
    def create(cls, key=None, **kwargs):
        assert key, "Key must be set"

        if not (obj := cls.get(key)):
            obj = cls(key, **kwargs)
            obj.id = key_collection.insert_one(obj.to_dict()).inserted_id

        return obj

    @classmethod
    def get(cls, key):
        key = key_collection.find_one({"key": key})

        if key:
            return cls(**key)

    def to_dict(self):
        return {
            "key": self.key,
            "description": self.description
        }

    def __repr__(self):
        return f"<Key: {self.key}>"

    @classmethod
    def list_prefix(cls, prefix):
        return cls.list(key={"$regex": prefix.replace(".", "[.]") + ".*"})

    @classmethod
    def list(cls, **kwargs):
        return [
            cls(**key)
            for key in key_collection.find(kwargs)
        ]

    def update(self, **kwargs):
        self_data = self.to_dict()
        new_data = {**self_data, **kwargs}

        if self_data != new_data:
            key_collection.update_one({"key": self.key}, {"$set": new_data})

            self.__dict__.update(new_data)

    def delete(self):
        key_collection.delete_one({"key": self.key})
        measure_collection.delete_many({"key": self.key})

    @property
    def measures(self):
        return Measure.list(key=self.key)


class Measure:
    def __init__(self, key=None, _id=None, value=None, timestamp=None):
        self.id = _id
        self.key = key
        self.value = value
        self.timestamp = timestamp

    @classmethod
    def create(cls, key=None, value=None, timestamp=None):
        assert key, "Key must be set"
        assert value, "Value must be set"
        assert timestamp, "Timestamp must be set"

        if not (obj := cls.get(key, timestamp=timestamp)):
            obj = cls(key, value=value, timestamp=timestamp)
            obj.id = measure_collection.insert_one(obj.to_dict()).inserted_id

        return obj

    @classmethod
    def get(cls, key, **kwargs):
        measure = measure_collection.find_one(
            {"key": key, **kwargs},
            sort=[("timestamp", -1)]
        )

        if measure:
            return cls(**measure)

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        return f"<Measure: {self.key} {self.timestamp}:{self.value}>"

    @classmethod
    def list(cls, **kwargs):
        return [
            cls(**measure)
            for measure in measure_collection.find(kwargs)
        ]

    def update(self, **kwargs):
        self_data = self.to_dict()
        new_data = {**self_data, **kwargs}

        if self_data != new_data:
            measure_collection.update_one({"key": self.key}, {"$set": new_data})

            self.__dict__.update(new_data)

    def delete(self):
        measure_collection.delete_one({"key": self.key})
