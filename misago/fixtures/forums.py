from django.utils import timezone
from misago.models import Forum, Thread, Post 
from misago.utils.fixtures import load_monitor_fixture, update_monitor_fixture
from misago.utils.strings import slugify

monitor_fixture = {
                   'threads': (1, 'int'),
                   'posts': (1, 'int'),
                  }

def load():
    Forum(special='private_threads', name='private', slug='private', type='forum').insert_at(None, save=True)
    Forum(special='reports', name='reports', slug='reports', type='forum').insert_at(None, save=True)

    root = Forum(special='root', name='root', slug='root')
    root.insert_at(None, save=True)
    cat = Forum(type='category', name='First Category', slug='first-category')
    cat.insert_at(root, save=True)
    forum = Forum(type='forum', name='First Forum', slug='first-forum', threads=1, posts=1)
    forum.insert_at(cat, save=True)
    Forum(type='redirect', name='Project Homepage', slug='project-homepage', redirect='http://misago-project.org').insert_at(cat, position='last-child', save=True)
    Forum.objects.populate_tree(True)

    now = timezone.now()
    thread = Thread.objects.create(
                                   forum=forum,
                                   name='Welcome to Misago!',
                                   slug=slugify('Welcome to Misago!'),
                                   start=now,
                                   last=now,
                                   )
    post = Post.objects.create(
                               forum=forum,
                               thread=thread,
                               user_name='MisagoProject',
                               ip='127.0.0.1',
                               agent='',
                               post='Welcome to Misago!',
                               post_preparsed='Welcome to Misago!',
                               date=now,
                               )
    thread.start_post = post
    thread.start_poster_name = 'MisagoProject'
    thread.start_poster_slug = 'misagoproject'
    thread.last_post = post
    thread.last_poster_name = 'MisagoProject'
    thread.last_poster_slug = 'misagoproject'
    thread.save(force_update=True)
    forum.last_thread = thread
    forum.last_thread_name = thread.name
    forum.last_thread_slug = thread.slug
    forum.last_thread_date = thread.last
    forum.last_poster = thread.last_poster
    forum.last_poster_name = thread.last_poster_name
    forum.last_poster_slug = thread.last_poster_slug
    forum.save(force_update=True)

    load_monitor_fixture(monitor_fixture)


def update():
    update_monitor_fixture(monitor_fixture)