import os
from typing import Any, List

from ariadne import SchemaBindable, load_schema_from_path, make_executable_schema

from .mutations import mutations
from .scalars import scalars
from .types import types


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(BASE_DIR, "schema")

type_defs = load_schema_from_path(SCHEMA_DIR)

schema_types: List[SchemaBindable] = []
schema_types += types
schema_types += mutations
schema_types += scalars

schema = make_executable_schema(type_defs, schema_types)
