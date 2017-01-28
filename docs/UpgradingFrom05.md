Upgrading from Misago 0.5
=========================

Misago 0.6 comes with special utility that allows those upgrading from Misago 0.5 to move their data to new site. This utility, named `datamover`, provides set of management commands allowing you to move data over.


##### Note:

If you are already familiar with migration process, Misago comes with special `runmigration` command that calls all required commands for you.


## Preparing for move

To move your data to new site, you'll need to first install Misago 0.6, and then tell mover how to access your old data.


### Database

In your site's `settings.py` find `DATABASES` setting, and add connection named `misago05`:

```python
DATABASES = {
    'default': {
        # new database used by Misago
    },
    'misago05': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_misago_05_database_name',
        'USER': 'your_misago_05_database_user',
        'PASSWORD': 'your_misago_05_database_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```


### User uploads

You'll actually won't need all of your old forum's files for move, only attachments and media directories. To tell data mover where it can find those directories, add `MISAGO_OLD_FORUM` setting somewhere in your `settings.py`, just like in example below:

```python
MISAGO_OLD_FORUM = {
    'ATTACHMENTS': '/home/somewhere/myoldmisago/attachments/',
    'MEDIA': '/home/somewhere/myoldmisago/media/',
}
```


### Creating superuser

Its good idea to create superuser accounts for all site administrators. Don't worry about their e-mails being same as ones on old forum. If this happens Misago will simply reuse those accounts, instead of creating new ones. 


## Moving forum configuration

To move configuration over to new forum, run `python manage.py movesettings` command.


##### Note:

Some settings have been moved from admin to configuration file or removed. Those will not be migrated. Please consult the [reference](./settings/README.md) for available settings that you will need to add yourself.


## Moving users

To move users over to new forum, run `python manage.py moveusers` command.

Moved users will be assigned default rank and permissions as those aren't moved by the datamover. If user with such e-mail address already exists in database (because you've used this e-mail ealier to create superuser account), his or her permissions and rank will be left as they are in new database.

If user avatar could not be moved (for .eg because uploaded picture is smaller than allowed by `MISAGO_AVATARS_SIZES`), default avatar will be set for this user.

In case of username collision, Misago will append digits to new user's username and print a warning in console to let you know about this.


## Moving threads

To move threads and categories over, run following commands:

    python manage.py movecategories
    python manage.py movethreads

This will move first the categories and then threads, posts, polls, attachments and finally private threads. This step will also take care of updating your posts markup.


## Wrapping up migration

Not everything is moved over. Thread labels will be turned into subcategories of their categories. With exception of pre-made superuser accounts, all users will be assigned to "Members" rank and will have only default roles of forum members. Likewise no permissions will be moved over to users, categories or ranks, and you will have to reset those manually. Reports, events, subscriptions and read tracker will also be omitted by migration.


### Recounting data

After moving users data over to new site, you'll need to rebuild their stats, trackers and bans. To do this use `invalidatebans`, `populateonlinetracker` and `synchronizeusers` commands that you can run via `manage.py`.

Likewise you'll need to rebuild threads and categories via `synchronizethreads`, then `synchronizecategories` and `rebuildpostssearch`.


### Changed links

Links in Misago have changed with 0.6 release, but Misago will not update posted url's for you. Instead it comes with small utility that will catch old urls and return 301 (permament) redirect to new url, keeping old urls alive.

To enable this feature you'll need to insert new url in your forum's `urls.py`, so it looks like this:

```python
    urlpatterns = [
        # insert below line above url with namespace='misago'
        url(r'^', include('misago.datamover.urls')),
        url(r'^', include('misago.urls', namespace='misago')),

        # ...rest of entries
    ]
```

Now build redirects index running `buildmovesindex` command. This will make Misago redirect users from old urls to new ones, altrough it'll wont preserve the meaning:

- All links to forum will redirect to category's start page
- All links to different profile pages of user profile will redirect to user's profile start page
- All links to thread will lead to thread's first page
- All links to post will lead to redirect to post in thread view

This script also comes with one limitation: Because it comes before Misago's urls, it will catch all requests to ranks whose names end with number and try to map them to old user profiles. This means that naming the rank "Squadron 42" will produce url `/users/squadron-42/` that will be interpreted as link to old user. To avoid this make sure your ranks names end with non-alphametical characters, eg. "Squadron 42th" will produce `/users/squardon-42th/` as link that will successfully resolve to rank.