from misago.monitor.fixtures import load_monitor_fixture

monitor_fixtures = {
                  'threads': 0,
                  'posts': 0,
                  }


def load_fixture():
    load_monitor_fixture(monitor_fixtures)