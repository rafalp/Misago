from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('Misago',
             broker='redis://',
             )

if __name__ == '__main__':
    app.start()
