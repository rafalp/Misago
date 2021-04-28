from ..forumstats import get_forum_stats
from ..graphql import GraphQLContext

CACHE_NAME = "__forum_stats"


async def load_forum_stats(context: GraphQLContext) -> dict:
    if CACHE_NAME not in context:
        context[CACHE_NAME] = await get_forum_stats()
    return context[CACHE_NAME]
