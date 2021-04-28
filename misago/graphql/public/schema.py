import os

from ariadne import load_schema_from_path, make_executable_schema

from ..hooks import graphql_directives_hook, graphql_type_defs_hook, graphql_types_hook
from ..shared.scalars import shared_scalars
from ..shared.schema import shared_type_defs
from ..shared.types import shared_types
from .mutations import mutations
from .subscriptions import subscriptions
from .types import types

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(BASE_DIR, "schema")

public_type_defs = load_schema_from_path(SCHEMA_DIR)

public_schema = make_executable_schema(
    [shared_type_defs, public_type_defs, *graphql_type_defs_hook],
    *shared_scalars,
    *shared_types,
    *types,
    *mutations,
    *subscriptions,
    *graphql_types_hook,
    directives=graphql_directives_hook
)
