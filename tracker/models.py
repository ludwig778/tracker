from tracker.repository import key_collection, measure_collection


class Key:
    def __init__(self, name=None, _id=None, description=None):
        self.id = _id
        self.name = name
        self.description = description

    @classmethod
    def create(cls, name=None, **kwargs):
        assert name, "Key must be set"

        if not (obj := cls.get(name)):
            obj = cls(name, **kwargs)
            obj.id = key_collection.insert_one(obj.to_dict()).inserted_id

        return obj

    @classmethod
    def get(cls, name):
        key = key_collection.find_one({"name": name})

        if key:
            return cls(**key)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description
        }

    def __repr__(self):
        return f"<Key: {self.name}>"

    @classmethod
    def list_prefix(cls, prefix):
        return cls.list(name={"$regex": prefix.replace(".", "[.]") + ".*"})

    @classmethod
    def list(cls, **kwargs):
        return [
            cls(**key)
            for key in key_collection.find(kwargs)
        ]

    def update(self, name=None, **kwargs):
        self_data = self.to_dict()
        new_data = {**self_data, **kwargs}

        if self_data != new_data:
            key_collection.update_one({"name": self.name}, {"$set": new_data})

            self.__dict__.update(new_data)

        if name and name != self.name:
            key_collection.update_one({"name": self.name}, {"$set": {"name": name}})

            self.name = name

    def rename(self, name):
        self.update(name=name)

    def delete(self):
        key_collection.delete_one({"name": self.name})
        measure_collection.delete_many({"key": self.name})

    @property
    def measures(self):
        return self.get_measures()

    def get_measures(self, **kwargs):
        return Measure.list(key=self.name, **kwargs)

    def get_latest_measure(self):
        return Measure.latest(key=self.name)

    def add_measure(self, **kwargs):
        return Measure.create(key=self.name, **kwargs)


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
    def list(cls, limit=50, **kwargs):
        cursor = (
            measure_collection
            .find(kwargs)
            .sort("timestamp", -1)
        )

        if limit:
            cursor = cursor.limit(limit)

        return [
            cls(**measure)
            for measure in sorted(
                cursor,
                key=lambda x: x["timestamp"]
            )
        ]

    @classmethod
    def rename(cls, old_name, new_name):
        measures = cls.list(key=old_name, limit=None)

        for measure in measures:
            measure.update(key=new_name)

    @classmethod
    def latest(cls, **kwargs):
        latest = list(measure_collection.find(kwargs).sort("timestamp", -1).limit(1))

        if latest:
            return cls(**latest[0])

    def update(self, **kwargs):
        self_data = self.to_dict()
        new_data = {**self_data, **kwargs}

        if self_data != new_data:
            measure_collection.update_one(
                {
                    "key": self.key,
                    "timestamp": self.timestamp
                }, {
                    "$set": new_data
                }
            )

            self.__dict__.update(new_data)

    def delete(self):
        measure_collection.delete_one({"key": self.key, "timestamp": self.timestamp})
