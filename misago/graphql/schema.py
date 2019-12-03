import os

from ariadne import load_schema_from_path, make_executable_schema

from ..hooks import graphql_directives_hook, graphql_type_defs_hook, graphql_types_hook
from .mutations import mutations
from .scalars import scalars
from .types import types


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(BASE_DIR, "schema")

type_defs = load_schema_from_path(SCHEMA_DIR)

schema = make_executable_schema(
    [type_defs, *graphql_type_defs_hook],
    *scalars,
    *types,
    *mutations,
    *graphql_types_hook,
    directives=graphql_directives_hook
)
