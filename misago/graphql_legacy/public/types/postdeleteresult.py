from typing import Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ....threads.loaders import posts_loader
from ....threads.models import Thread
from ...cleanargs import clean_page_arg, invalid_args_handler

post_delete_mutation_result = ObjectType("PostDeleteMutationResult")
posts_bulk_delete_mutation_result = ObjectType("PostsBulkDeleteMutationResult")


@post_delete_mutation_result.field("posts")
@posts_bulk_delete_mutation_result.field("posts")
@invalid_args_handler
async def resolve_posts(result: dict, info: GraphQLResolveInfo, *, page: int = 1):
    page = clean_page_arg(page)

    thread: Optional[Thread] = result.get("thread")
    if not thread:
        return None

    paginator = await posts_loader.load_paginator(info.context, thread.id)
    if not paginator:
        return None

    return await paginator.get_page(page)
