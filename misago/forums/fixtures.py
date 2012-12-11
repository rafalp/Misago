from misago.monitor.fixtures import load_monitor_fixture
from misago.forums.models import Forum

monitor_fixtures = {
                  'threads': 0,
                  'posts': 0,
                  }


def load_fixtures():
    load_monitor_fixture(monitor_fixtures)
    
    root_forum = Forum(
                       token='root',
                       name='root',
                       slug='root',
                       )
    Forum.objects.insert_node(root_forum,target=None,save=True)