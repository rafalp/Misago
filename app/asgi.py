import os

from misago import get_asgi_application, setup


os.environ.setdefault("MISAGO_SETTINGS_MODULE", "app.settings")

setup()

app = get_asgi_application()
