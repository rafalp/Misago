from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import connections
from misago.models import *

class Command(BaseCommand):
    """
    Small utility that migrates data from Misago 0.1 instalation to 0.2
    """
    help = 'Updates Popular Threads ranking'
    def handle(self, *args, **options):
        self.cursor = connections['deprecated'].cursor()
        self.stdout.write('\nBeginning migration from Misago 0.1...\n')

        self.mig_settings()
        self.mig_monitor()

        self.users = {}
        self.forums = {}
        self.threads = {}

        self.mig_users()
        self.mig_users_roles()
        self.mig_users_relations()
        
        Karma.objects.all().delete()
        Change.objects.all().delete()
        Checkpoint.objects.all().delete()
        Post.objects.all().delete()
        Thread.objects.all().delete()

        self.mig_forums()
        
        self.mig_threads()
        self.mig_posts()
        self.mig_subs()

        self.sync_threads()
        self.sync_forums()
        
        self.stdout.write('\nData was migrated.\n')

    def mig_settings(self):
        self.stdout.write('Migrating Database Settings...')
        self.cursor.execute("SELECT setting, value FROM settings_setting");
        for row in self.dictfetchall():
            Setting.objects.filter(setting=row['setting']).update(value=row['value'])

    def mig_monitor(self):
        self.stdout.write('Migrating Forum Monitor...')
        self.cursor.execute("SELECT id, value, updated FROM monitor_item");
        for row in self.dictfetchall():
            MonitorItem.objects.filter(id=row['id']).update(value=row['value'], updated=row['updated'])

    def mig_users(self):
        User.objects.all().delete()
        self.stdout.write('Migrating Users...')
        self.cursor.execute("SELECT * FROM users_user");
        for row in self.dictfetchall():
            self.users[row['id']] = User.objects.create(
                                                        username=row['username'],
                                                        username_slug=row['username_slug'],
                                                        email=row['email'],
                                                        email_hash=row['email_hash'],
                                                        password=row['password'],
                                                        password_date=row['password_date'],
                                                        avatar_type=row['avatar_type'],
                                                        avatar_image=row['avatar_image'],
                                                        avatar_original=row['avatar_original'],
                                                        avatar_temp=row['avatar_temp'],
                                                        signature=row['signature'],
                                                        signature_preparsed=row['signature_preparsed'],
                                                        join_date=row['join_date'],
                                                        join_ip=row['join_ip'],
                                                        join_agent=row['join_agent'],
                                                        last_date=row['last_date'],
                                                        last_ip=row['last_ip'],
                                                        last_agent=row['last_agent'],
                                                        hide_activity=row['hide_activity'],
                                                        subscribe_start=row['subscribe_start'],
                                                        subscribe_reply=row['subscribe_reply'],
                                                        receive_newsletters=row['receive_newsletters'],
                                                        threads=row['threads'],
                                                        posts=row['posts'],
                                                        votes=row['votes'],
                                                        karma_given_p=row['karma_given_p'],
                                                        karma_given_n=row['karma_given_n'],
                                                        karma_p=row['karma_p'],
                                                        karma_n=row['karma_n'],
                                                        following=row['following'],
                                                        followers=row['followers'],
                                                        score=row['score'],
                                                        ranking=row['ranking'],
                                                        last_sync=row['last_sync'],
                                                        title=row['title'],
                                                        last_post=row['last_post'],
                                                        last_search=row['last_search'],
                                                        alerts=row['alerts'],
                                                        alerts_date=row['alerts_date'],
                                                        activation=row['activation'],
                                                        token=row['token'],
                                                        avatar_ban=row['avatar_ban'],
                                                        avatar_ban_reason_user=row['avatar_ban_reason_user'],
                                                        avatar_ban_reason_admin=row['avatar_ban_reason_admin'],
                                                        signature_ban=row['signature_ban'],
                                                        signature_ban_reason_user=row['signature_ban_reason_user'],
                                                        signature_ban_reason_admin=row['signature_ban_reason_admin'],
                                                        timezone=row['timezone'],
                                                        is_team=row['is_team'],
                                                        acl_key=row['acl_key'],
                                                        )

    def mig_users_roles(self):
        self.stdout.write('Migrating Users Roles...')
        self.cursor.execute("SELECT * FROM users_user_roles");
        for row in self.dictfetchall():
            self.users[row['user_id']].roles.add(Role.objects.get(id=row['role_id']))

    def mig_users_relations(self):
        self.stdout.write('Migrating Users Relations...')
        self.cursor.execute("SELECT * FROM users_user_follows");
        for row in self.dictfetchall():
            self.users[row['from_user_id']].follows.add(self.users[row['to_user_id']])
        self.cursor.execute("SELECT * FROM users_user_ignores");
        for row in self.dictfetchall():
            self.users[row['from_user_id']].ignores.add(self.users[row['to_user_id']])

    def mig_forums(self):
        self.stdout.write('Migrating Forums...')
        self.forums[4] = Forum.objects.get(special='root')
        for forum in self.forums[4].get_descendants():
            forum.delete()
        self.forums[4] = Forum.objects.get(special='root')
        self.cursor.execute("SELECT * FROM forums_forum WHERE level > 0 ORDER BY lft");
        for row in self.dictfetchall():
            self.forums[row['id']] = Forum(
                                           type=row['type'],
                                           special=row['token'],
                                           name=row['name'],
                                           slug=row['slug'],
                                           description=row['description'],
                                           description_preparsed=row['description_preparsed'],
                                           redirect=row['redirect'],
                                           attrs=row['attrs'],
                                           show_details=row['show_details'],
                                           style=row['style'],
                                           closed=row['closed'],
                                           )
            self.forums[row['id']].insert_at(self.forums[row['parent_id']], position='last-child', save=True)
            Forum.objects.populate_tree(True)

    def mig_threads(self):
        self.stdout.write('Migrating Threads...')
        self.cursor.execute("SELECT * FROM threads_thread");
        for row in self.dictfetchall():
            self.threads[row['id']] = Thread.objects.create(                
                                                            forum=self.forums[row['forum_id']],
                                                            weight=row['weight'],
                                                            name=row['name'],
                                                            slug=row['slug'],
                                                            merges=row['merges'],
                                                            score=row['score'],
                                                            upvotes=row['upvotes'],
                                                            downvotes=row['downvotes'],
                                                            start=row['start'],
                                                            start_poster_name='a',
                                                            start_poster_slug='a',
                                                            last=row['last'],
                                                            deleted=row['deleted'],
                                                            closed=row['closed'],
                                                            )

    def mig_posts(self):
        self.stdout.write('Migrating Posts...')
        self.cursor.execute("SELECT * FROM threads_post");
        for row in self.dictfetchall():
            post = Post.objects.create(
                                       forum=self.forums[row['forum_id']],
                                       thread=self.threads[row['thread_id']],
                                       merge=row['merge'],
                                       user=(self.users[row['user_id']] if row['user_id'] else None),
                                       user_name=row['user_name'],
                                       ip=row['ip'],
                                       agent=row['agent'],
                                       post=row['post'],
                                       post_preparsed=row['post_preparsed'],
                                       upvotes=row['upvotes'],
                                       downvotes=row['downvotes'],
                                       checkpoints=row['checkpoints'],
                                       date=row['date'],
                                       edits=row['edits'],
                                       edit_date=row['edit_date'],
                                       edit_reason=row['edit_reason'],
                                       edit_user=(self.users[row['edit_user_id']] if row['edit_user_id'] else None),
                                       edit_user_name=row['edit_user_name'],
                                       edit_user_slug=row['edit_user_slug'],
                                       reported=row['reported'],
                                       moderated=row['moderated'],
                                       deleted=row['deleted'],
                                       protected=row['protected'],
                                       )

            # Migrate post checkpoints
            self.cursor.execute("SELECT * FROM threads_checkpoint WHERE post_id = %s" % row['id']);
            for related in self.dictfetchall():
                Checkpoint.objects.create(
                                          forum=self.forums[row['forum_id']],
                                          thread=self.threads[row['thread_id']],
                                          post=post,
                                          action=related['action'],
                                          user=(self.users[related['user_id']] if related['user_id'] else None),
                                          user_name=related['user_name'],
                                          user_slug=related['user_slug'],
                                          date=related['date'],
                                          ip=related['ip'],
                                          agent=related['agent'],
                                          )

            # Migrate post edits
            self.cursor.execute("SELECT * FROM threads_change WHERE post_id = %s" % row['id']);
            for related in self.dictfetchall():
                Change.objects.create(
                                      forum=self.forums[row['forum_id']],
                                      thread=self.threads[row['thread_id']],
                                      post=post,
                                      user=(self.users[related['user_id']] if related['user_id'] else None),
                                      user_name=related['user_name'],
                                      user_slug=related['user_slug'],
                                      date=related['date'],
                                      ip=related['ip'],
                                      agent=related['agent'],
                                      reason=related['reason'],
                                      thread_name_new=related['thread_name_new'],
                                      thread_name_old=related['thread_name_old'],
                                      post_content=related['post_content'],
                                      size=related['size'],
                                      change=related['change'],
                                      )

            # Migrate post karmas
            self.cursor.execute("SELECT * FROM threads_karma WHERE post_id = %s" % row['id']);
            for related in self.dictfetchall():
                Karma.objects.create(
                                     forum=self.forums[row['forum_id']],
                                     thread=self.threads[row['thread_id']],
                                     post=post,
                                     user=(self.users[related['user_id']] if related['user_id'] else None),
                                     user_name=related['user_name'],
                                     user_slug=related['user_slug'],
                                     date=related['date'],
                                     ip=related['ip'],
                                     agent=related['agent'],
                                     score=related['score'],
                                     )

            # Migrate mentions
            self.cursor.execute("SELECT * FROM threads_post_mentions WHERE post_id = %s" % row['id']);
            for related in self.dictfetchall():
                post.mentions.add(self.users[related['user_id']])

    def mig_subs(self):
        self.stdout.write('Migrating Subscribtions...')
        self.cursor.execute("SELECT * FROM watcher_threadwatch");
        for row in self.dictfetchall():
            WatchedThread.objects.create( 
                                         user=self.users[row['user_id']],
                                         forum=self.forums[row['forum_id']],
                                         thread=self.threads[row['thread_id']],
                                         last_read=row['last_read'],
                                         email=row['email'],
                                         )

    def sync_threads(self):
        self.stdout.write('Synchronising Threads...')
        for thread in Thread.objects.all():
            thread.sync()
            thread.save(force_update=True)

    def sync_forums(self):
        self.stdout.write('Synchronising Forums...')
        for forum in Forum.objects.all():
            forum.sync()
            forum.save(force_update=True)

    def dictfetchall(self):
        desc = self.cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in self.cursor.fetchall()]