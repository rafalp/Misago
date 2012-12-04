from django.conf import settings
from django.db import models, connection, transaction
from django.utils.translation import ugettext_lazy as _

class Rank(models.Model):
    """
    Misago User Rank
    Ranks are ready style/title pairs that are assigned to users either by admin (special ranks) or as result of user activity.
    """
    name = models.CharField(max_length=255)
    name_slug = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    style = models.CharField(max_length=255,null=True,blank=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    special = models.BooleanField(default=False)
    as_tab = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    criteria = models.CharField(max_length=255,null=True,blank=True)
    
    def __unicode__(self):
        return unicode(_(self.name))
    
    def assign_rank(self, users=0, special_ranks=None):
        if not self.criteria or self.special or users == 0:
            # Rank cant be rolled in
            return False
        
        if self.criteria == "0":
            # Just update all fellows
            User.objects.exclude(rank__in=special_ranks).update(rank=self)
        else:
            # Count number of users to update
            if self.criteria[-1] == '%':
                criteria = int(self.criteria[0:-1])
                criteria = int(math.ceil(float(users / 100.0)* criteria))
            else:
                criteria = int(self.criteria)
            
            # Join special ranks
            if special_ranks:
                special_ranks = ','.join(special_ranks)
            
            # Run raw query
            cursor = connection.cursor()
            try:
                # Postgresql
                if (settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
                    or settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql'):
                    if special_ranks:
                        cursor.execute('''UPDATE users_user
                            FROM (
                                SELECT id
                                FROM users_user
                                WHERE rank_id NOT IN (%s)
                                ORDER BY score DESC LIMIT %s
                                ) AS updateable
                            SET rank_id=%s
                            WHERE id = updateable.id
                            RETURNING *''' % (self.id, special_ranks, criteria))
                    else:
                        cursor.execute('''UPDATE users_user
                            FROM (
                                SELECT id
                                FROM users_user
                                ORDER BY score DESC LIMIT %s
                                ) AS updateable
                            SET rank_id=%s
                            WHERE id = updateable.id
                            RETURNING *''', [self.id, criteria])
                        
                # MySQL, SQLite and Oracle
                if (settings.DATABASES['default']['ENGINE'] == 'django.db.backends.mysql'
                    or settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3'
                    or settings.DATABASES['default']['ENGINE'] == 'django.db.backends.oracle'):
                    if special_ranks:
                        cursor.execute('''UPDATE users_user
                            SET rank_id=%s
                            WHERE rank_id NOT IN (%s)
                            ORDER BY score DESC
                            LIMIT %s''' % (self.id, special_ranks, criteria))
                    else:
                        cursor.execute('''UPDATE users_user
                        SET rank_id=%s
                        ORDER BY score DESC
                        LIMIT %s''', [self.id, criteria])
            except Exception as e:
                print 'Error updating users ranking: %s' % e
            transaction.commit_unless_managed()
        return True