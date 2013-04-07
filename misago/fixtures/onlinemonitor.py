from misago.utils.fixtures import load_monitor_fixture

monitor_fixture = {
                   'online_members': 0,
                   'online_all': 0,
                  }


def load():
    load_monitor_fixture(monitor_fixture)