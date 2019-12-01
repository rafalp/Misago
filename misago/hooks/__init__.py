from .action import ActionHook
from .filter import FilterHook
from .filters import (
    CreateUserHook,
    GraphQLContextHook,
    RegisterInputHook,
    RegisterInputModelHook,
    RegisterUserHook,
)


create_user_hook = CreateUserHook()
graphql_context_hook = GraphQLContextHook()
register_input_hook = RegisterInputHook()
register_input_model_hook = RegisterInputModelHook()
register_user_hook = RegisterUserHook()
