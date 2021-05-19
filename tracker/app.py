from datetime import datetime, timedelta

from tabulate import tabulate

from tracker.display import plot_measures
from tracker.models import Key, Measure
from tracker.parser import get_args


class App:
    def __init__(self):
        self.args = get_args()

    def run(self):
        key = Key.get(self.args.key)

        if self.args.delete:
            if key and (self.args.timestamp or self.args.date):
                self.delete_measure(key)

            elif key:
                self.delete_key(key)

        elif self.args.value or self.args.incr:
            self.handle_measure(key)

        elif self.args.key and not key:

            if self.args.empty:
                self.create_key(self.args.key)

            else:
                self.handle_non_existing_key(self.args.key)

        elif key and not self.args.value:
            self.show_measures(key)

        else:
            self.show_keys()

    def get_args_timestamp(self, strict=False):
        if self.args.timestamp:
            return self.args.timestamp
        elif self.args.date:
            return int(datetime.strptime(self.args.date, "%Y-%m-%d").strftime("%s"))
        elif strict:
            return
        else:
            return int(datetime.now().strftime("%s"))

    def delete_measure(self, key):
        timestamp = self.get_args_timestamp(strict=True)

        measures = key.get_measures(timestamp={"$eq": timestamp}, limit=None)

        if measures:
            measures[0].delete()

    def delete_key(self, key):
        if input(f"Are you sure to delete {key} ? [y/N] ").lower() == "y":
            key.delete()

    def create_key(self, key):
        Key.create(name=key)

        print("Empty key created")

    def handle_measure(self, key):
        if not key:
            key = Key.create(name=self.args.key)

        now = datetime.now()
        if self.args.day:
            now = now.replace(hour=0, minute=0, second=0, microsecond=0)

        timestamp = self.get_args_timestamp()

        if self.args.incr:
            if measure := Measure.get(key=key.name, timestamp=timestamp):
                measure.update(value=measure.value + 1)
                print("Measure incremented to", measure.value)
            else:
                measure = Measure.create(key=key.name, value=1, timestamp=timestamp)
                print("Measure added")
        else:
            if measure := Measure.get(key=key.name, timestamp=timestamp):
                measure.update(value=int(self.args.value))
                print("Measure updated")
            else:
                measure = key.add_measure(
                    value=int(self.args.value),
                    timestamp=timestamp
                )
                print("Measure added")

        self.show_measures(key)

    def handle_non_existing_key(self, key):
        keys = Key.list_prefix(key)

        if not keys:
            print("No values found")
            return

        data = []
        for key in sorted(Key.list(), key=lambda k: k.name):
            last_measure = key.get_latest_measure()
            last_value = last_measure.value if last_measure else None

            data.append({
                "key": key.name,
                "value": last_value
            })

        print(tabulate(data, tablefmt="simple"))

    def show_measures(self, key):
        timestamp = int((datetime.now() - timedelta(days=7)).strftime("%s"))

        measures = key.get_measures(
            limit=None,
            timestamp={"$gt": timestamp}
        )

        if self.args.raw:
            for measure in measures:
                print(
                    datetime.fromtimestamp(measure.timestamp),
                    measure.timestamp,
                    measure.value
                )

        elif not measures:
            latest = key.get_latest_measure()

            if latest:
                print(f"Latest measure {datetime.fromtimestamp(latest.timestamp)}: value : {latest.value}")
            else:
                print("No measures")

        else:
            plot_measures(measures)

    def show_keys(self):
        print(tabulate([
            [k]
            for k in sorted(map(lambda k: k.name, Key.list()))
        ]))
