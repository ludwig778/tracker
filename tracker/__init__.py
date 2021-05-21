from tracker.app import App


def main():
    try:
        App().run()
    except KeyboardInterrupt:
        pass
