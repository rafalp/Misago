from misago.monitor.fixtures import load_monitor_fixture
from misago.forums.models import Forum

def load_fixtures():
    anno = Forum(token='annoucements', name='annoucements', slug='annoucements', type='forum').insert_at(target=None,save=True)
    Forum(token='private', name='private', slug='private', type='forum').insert_at(target=None,save=True)
    Forum(token='reports', name='reports', slug='reports', type='forum').insert_at(target=None,save=True)
    Forum(token='root', name='root', slug='root').insert_at(target=None,save=True)
    
    load_monitor_fixture({
                          'threads': 0,
                          'posts': 0,
                          'anno': anno.pk
                          })