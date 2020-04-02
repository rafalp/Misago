import os

from ariadne import load_schema_from_path, make_executable_schema

from ...hooks import (
    graphql_admin_directives_hook,
    graphql_admin_type_defs_hook,
    graphql_admin_types_hook,
    graphql_directives_hook,
    graphql_type_defs_hook,
    graphql_types_hook,
)
from ..mutations import mutations
from ..scalars import scalars
from ..schema import type_defs
from ..types import types


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(BASE_DIR, "schema")

admin_type_defs = load_schema_from_path(SCHEMA_DIR)

admin_schema = make_executable_schema(
    [
        type_defs,
        admin_type_defs,
        *graphql_type_defs_hook,
        *graphql_admin_type_defs_hook,
    ],
    *scalars,
    *types,
    *mutations,
    *graphql_types_hook,
    *graphql_admin_types_hook,
    directives={**graphql_directives_hook, **graphql_admin_directives_hook},
)
