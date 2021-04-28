import asyncio
from typing import Any

from ..database.queries import update
from ..tables import settings
from .types import Settings


async def update_settings(settings: Settings):
    operations = [update_setting(setting, value) for setting, value in settings.items()]
    if operations:
        await asyncio.gather(*operations)


async def update_setting(setting: str, value: Any):
    await update(settings, setting, value=value)
