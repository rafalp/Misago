from misago.utils.fixtures import load_monitor_fixture, update_monitor_fixture

monitor_fixture = {
                   'users': (0, 'int'),
                   'users_inactive': (0, 'int'),
                   'last_user': ('', 'string'),
                   'last_user_name': ('', 'string'),
                   'last_user_slug': ('', 'string'),
                  }


def load():
    load_monitor_fixture(monitor_fixture)


def update():
    update_monitor_fixture(monitor_fixture)