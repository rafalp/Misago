from graphql import GraphQLResolveInfo

from ...threads.loaders import posts_loader
from ..args import clean_page_arg, handle_invalid_args


@handle_invalid_args
async def resolve_posts_page(
    info: GraphQLResolveInfo, thread_id: int, *, page: int = 1
):
    page = clean_page_arg(page)
    paginator = await posts_loader.load_paginator(info.context, thread_id)
    if not paginator:
        return None

    return await paginator.get_page(page)
