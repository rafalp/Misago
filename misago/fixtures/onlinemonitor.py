from misago.utils.fixtures import load_monitor_fixture, update_monitor_fixture

monitor_fixture = {
                   'online_members': (0, 'int'),
                   'online_all': (0, 'int'),
                  }


def load():
    load_monitor_fixture(monitor_fixture)


def update():
    update_monitor_fixture(monitor_fixture)