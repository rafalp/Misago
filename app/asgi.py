import os

from misago.asgi import get_asgi_application


os.environ.setdefault("MISAGO_SETTINGS_MODULE", "app.settings")
app = get_asgi_application()
