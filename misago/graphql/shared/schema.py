import os

from ariadne import load_schema_from_path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(BASE_DIR, "schema")

shared_type_defs = load_schema_from_path(SCHEMA_DIR)
