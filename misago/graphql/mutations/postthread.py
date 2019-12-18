from ariadne import MutationType
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, constr

from ...auth import get_authenticated_user
from ...loaders import load_category
from ...threads.create import create_post, create_thread
from ...threads.update import update_thread
from ...validation import validate_model
from ...validation.errors import NotAuthorizedError
from ..errorhandler import error_handler


post_thread_mutation = MutationType()


@post_thread_mutation.field("postThread")
@error_handler
async def resolve_post_thread(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    user = await get_authenticated_user(info.context)
    if not user:
        raise NotAuthorizedError()

    data, errors = validate_model(PostThreadInput, input)
    if errors:
        return {"errors": errors}

    category = await load_category(info.context, data["category"])
    thread = await create_thread(category, data["title"], starter=user)
    post = await create_post(thread, {"text": data["body"]}, poster=user)
    thread = await update_thread(thread, first_post=post, last_post=post)

    return {"thread": thread}


class PostThreadInput(BaseModel):
    category: PositiveInt
    title: constr(strip_whitespace=True)
    body: constr(strip_whitespace=True)
