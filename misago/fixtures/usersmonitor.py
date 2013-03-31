from misago.utils.fixtures import load_monitor_fixture

monitor_fixture = {
                   'users': 0,
                   'users_inactive': 0,
                   'users_reported': 0,
                   'last_user': None,
                   'last_user_name': None,
                   'last_user_slug': None,
                  }


def load():
    load_monitor_fixture(monitor_fixture)