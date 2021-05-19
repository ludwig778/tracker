import argparse

import argcomplete

from tracker.models import Key


def KeyCompleter(prefix=None, **kwargs):
    return [key.name for key in Key.list_prefix(prefix)]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("key", nargs="?").completer = KeyCompleter
    parser.add_argument("value", nargs="?")
    parser.add_argument("--timestamp", action="store", type=int)
    parser.add_argument("--date", action="store")
    parser.add_argument("--incr", "-i", action="store_true")
    parser.add_argument("--day", "-t", action="store_true")
    parser.add_argument("--describe", "-e", action="store_true")
    parser.add_argument("--delete", "-d", action="store_true")
    parser.add_argument("--raw", "-r", action="store_true")
    argcomplete.autocomplete(parser)

    return parser.parse_args()
