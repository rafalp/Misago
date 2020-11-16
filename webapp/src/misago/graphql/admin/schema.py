import os

from ariadne import QueryType, load_schema_from_path, make_executable_schema

from .analytics import analytics
from .status import status
from .versioncheck import version_check

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(FILE_PATH, "schema.graphql")

type_defs = load_schema_from_path(SCHEMA_PATH)
schema = make_executable_schema(type_defs, [analytics, status, version_check])
