from django.db import models
import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Record(models.Model):
    user = models.ForeignKey('users.User')
    forum = models.ForeignKey('forums.Forum')
    threads = models.TextField(null=True,blank=True)
    updated = models.DateTimeField()
    cleared = models.DateTimeField()
    
    def get_threads(self):
        try:
            return pickle.loads(base64.decodestring(self.threads))
        except Exception:
            # ValueError, SuspiciousOperation, unpickling exceptions. If any of
            # these happen, just return an empty dictionary (an empty permissions list).
            return {}
    
    def set_threads(self, threads):
        self.threads = base64.encodestring(pickle.dumps(threads, pickle.HIGHEST_PROTOCOL))
    