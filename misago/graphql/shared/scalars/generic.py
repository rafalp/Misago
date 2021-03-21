from typing import Any

from ariadne import ScalarType

generic_scalar = ScalarType("Generic")


@generic_scalar.serializer
def serialize_generic_scalar(value: Any) -> Any:
    return value


@generic_scalar.literal_parser
def parse_generic_scalar_literal(value: Any, ast: Any = None) -> Any:
    return value
