from datetime import datetime, timedelta
from django.conf import settings

class CookieJar(object):
    def __init__(self):
        self._set_cookies = []
        self._delete_cookies = []

    def set(self, cookie, value, permanent=False):
        if permanent:
            # 360 days
            max_age = 31104000
        else:
            # 48 hours
            max_age = 172800
        self._set_cookies.append({
                                  'name': cookie,
                                  'value': value,
                                  'max_age': max_age,
                                  })

    def delete(self, cookie):
        self._delete_cookies.append(cookie)

    def flush(self, response):
        for cookie in self._set_cookies:
            response.set_cookie(
                                settings.COOKIES_PREFIX + cookie['name'],
                                cookie['value'],
                                max_age=cookie['max_age'],
                                path=settings.COOKIES_PATH,
                                domain=settings.COOKIES_DOMAIN,
                                secure=settings.COOKIES_SECURE
                                )

        for cookie in self._delete_cookies:
            response.delete_cookie(
                                   settings.COOKIES_PREFIX + cookie,
                                   path=settings.COOKIES_PATH,
                                   domain=settings.COOKIES_DOMAIN,
                                   )
