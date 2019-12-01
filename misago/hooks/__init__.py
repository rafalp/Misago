from .action import ActionHook
from .filter import FilterHook
from .filters import GraphQLContextHook, RegisterInputHook, RegisterInputModelHook


graphql_context_hook = GraphQLContextHook()
register_input_hook = RegisterInputHook()
register_input_model_hook = RegisterInputModelHook()
