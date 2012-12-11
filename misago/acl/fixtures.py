from misago.monitor.fixtures import load_monitor_fixture

monitor_fixtures = {
                  'acl_version': 0,
                  }


def load_fixtures():
    load_monitor_fixture(monitor_fixtures)