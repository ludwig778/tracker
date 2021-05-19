from datetime import datetime
from pprint import pprint as pp

from tracker.models import Key, Measure
from tracker.parser import get_args


class App:
    def __init__(self):
        self.args = get_args()

    def run(self):
        key = Key.get(self.args.key)

        if self.args.delete:
            if key and self.args.timestamp:
                self.delete_measure(key, self.args.timestamp)

            elif key:
                self.delete_key(key)

        elif self.args.value or self.args.incr:
            self.handle_measure(key)

        elif self.args.key and not key:
            print("MUST SET VALUE")

        elif key and not self.args.value:
            self.show_measures(key)

        else:
            self.show_keys()

    def delete_measure(self, key, timestamp):
        measures = key.get_measures(timestamp=timestamp, limit=None)

        if measures:
            measures[0].delete()

    def delete_key(self, key):
        if input(f"Are you sure to delete {key} ? [y/N] ").lower() == "y":
            key.delete()

    def handle_measure(self, key):
        if not key:
            key = Key.create(name=self.args.key)

        now = datetime.now()
        if self.args.day:
            now = now.replace(hour=0, minute=0, second=0, microsecond=0)

        timestamp = self.args.timestamp or int(now.strftime("%s"))

        if self.args.incr:
            if measure := Measure.get(key=key.name, timestamp=timestamp):
                measure.update(value=measure.value + 1)
                print("MEASURE INCREMENTED", key, measure)
            else:
                measure = Measure.create(key=key.name, value=1, timestamp=timestamp)
                print("MEASURE ADDED", key, measure)
        else:
            measure = key.add_measure(
                value=int(self.args.value),
                timestamp=timestamp
            )
            print("MEASURE ADDED", key, measure)

    def show_measures(self, key):
        print("SHOW MEASURES")
        pp(key.measures)

    def show_keys(self):
        for k in sorted(map(lambda k: k.name, Key.list())):
            print(k)
