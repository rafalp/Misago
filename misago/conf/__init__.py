import os
from typing import Dict, cast

from .staticsettings import StaticSettings


SETTINGS_CACHE = "settings"


settings = StaticSettings(cast(Dict, os.environ))
