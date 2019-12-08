from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt
from jwt.exceptions import InvalidTokenError

from ..hooks import create_user_token_payload_hook
from ..types import GraphQLContext, User
from ..users.get import get_user_by_id


JWT_ALGORITHM = "HS256"


async def create_user_token(context: GraphQLContext, user: User) -> bytes:
    secret = get_jwt_secret(context)
    payload = await create_user_token_payload_hook.call_action(
        create_user_token_payload, context, user
    )
    return encode_token(secret, payload)


async def create_user_token_payload(
    context: GraphQLContext, user: User
) -> Dict[str, Any]:
    return {"exp": get_jwt_exp(context), "user": user["id"]}


def get_jwt_exp(context: GraphQLContext) -> datetime:
    return datetime.now() + timedelta(seconds=context["settings"]["jwt_exp"])


async def get_user_from_token(context: GraphQLContext, token: bytes) -> Optional[User]:
    secret = get_jwt_secret(context)
    token_payload = decode_token(secret, token)
    if not token_payload:
        return None

    return await get_user_by_id(token_payload["user"])


def get_jwt_secret(context: GraphQLContext) -> str:
    return context["settings"]["jwt_secret"]


def encode_token(secret: str, payload: Dict[str, Any]) -> bytes:
    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)


def decode_token(secret: str, token: bytes) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
    except InvalidTokenError:
        return None
