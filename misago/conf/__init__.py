import os
from typing import Dict, cast

from .staticsettings import StaticSettings

settings = StaticSettings(cast(Dict, os.environ))


__all__ = ["settings"]
