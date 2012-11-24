from misago.monitor.fixtures import load_monitor_fixture

monitor_fixtures = {
                  'threads': 0,
                  'posts': 0,
                  }


def load_fixtures():
    load_monitor_fixture(monitor_fixtures)