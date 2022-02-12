from ..context import Context
from ..loaders import simple_loader
from .forumstats import get_forum_stats


@simple_loader("forum_stats")
async def load_forum_stats(_: Context) -> dict:
    return await get_forum_stats()
