from django.db import models

BAN_NAME_EMAIL = 0
BAN_NAME = 1
BAN_EMAIL = 2
BAN_IP = 3

class BansManager(models.Manager):
    def check_ban(ip=False, username=False, email=False):
        bans_model = Ban.objects.filter(Q(expires=None) | Q(expires__gt=timezone.now()))
        if not (ip and username and email):
            if ip:
                bans_model.filter(test=BAN_IP)
            if username:
                bans_model.filter(test=BAN_NAME_EMAIL)
                bans_model.filter(test=BAN_NAME)
            if email:
                bans_model.filter(test=BAN_NAME_EMAIL)
                bans_model.filter(test=BAN_EMAIL)
        for ban in bans_model.order_by('-expires').iterator():
            if (
                # Check user name
                ((username and (ban.test == BAN_NAME_EMAIL or ban.test == BAN_NAME))
                and re.search('^' + re.escape(ban.ban).replace('\*', '(.*?)') + '$', username, flags=re.IGNORECASE))
                or # Check user email
                ((email and (ban.test == BAN_NAME_EMAIL or ban.test == BAN_EMAIL))
                and re.search('^' + re.escape(ban.ban).replace('\*', '(.*?)') + '$', email, flags=re.IGNORECASE))
                or # Check IP address
                (ip and ban.test == BAN_IP
                and re.search('^' + re.escape(ban.ban).replace('\*', '(.*?)') + '$', ip, flags=re.IGNORECASE))):
                    return ban
        return False


class Ban(models.Model):
    test = models.PositiveIntegerField(default=BAN_NAME_EMAIL)
    ban = models.CharField(max_length=255)
    reason_user = models.TextField(null=True, blank=True)
    reason_admin = models.TextField(null=True, blank=True)
    expires = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'misago'


class BanCache(object):
    def __init__(self):
        self.banned = False
        self.test = None
        self.expires = None
        self.reason_user = None
        self.version = 0

    def check_for_updates(self, request):
        if (self.version < request.monitor['bans_version']
            or (self.expires != None and self.expires < timezone.now())):
            self.version = request.monitor['bans_version']

            # Check Ban
            if request.user.is_authenticated():
                ban = check_ban(
                                ip=request.session.get_ip(request),
                                username=request.user.username,
                                email=request.user.email
                                )
            else:
                ban = check_ban(ip=request.session.get_ip(request))

            # Update ban cache
            if ban:
                self.banned = True
                self.reason_user = ban.reason_user
                self.expires = ban.expires
                self.test = ban.test
            else:
                self.banned = False
                self.reason_user = None
                self.expires = None
                self.test = None
            return True
        return False

    def is_banned(self):
        return self.banned
