from typing import Dict, List, Type

from ariadne import SchemaBindable, SchemaDirectiveVisitor

from .action import ActionHook
from .filter import FilterHook
from .filters import (
    CreateUserHook,
    CreateUserTokenHook,
    CreateUserTokenPayloadHook,
    GraphQLContextHook,
    RegisterInputHook,
    RegisterInputModelHook,
    RegisterUserHook,
)


create_user_hook = CreateUserHook()
create_user_token_hook = CreateUserTokenHook()
create_user_token_payload_hook = CreateUserTokenPayloadHook()
graphql_context_hook = GraphQLContextHook()
graphql_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_type_defs_hook: List[str] = []
graphql_types_hook: List[SchemaBindable] = []
register_input_hook = RegisterInputHook()
register_input_model_hook = RegisterInputModelHook()
register_user_hook = RegisterUserHook()
