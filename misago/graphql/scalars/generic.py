from typing import Any

from ariadne_graphql_modules import ScalarType, gql


class GenericScalar(ScalarType):
    __schema__ = gql("scalar Generic")

    @staticmethod
    def serialize(value: Any) -> Any:  # type: ignore
        return value

    @staticmethod
    def parse_literal(value: Any, variable_values: Any = None) -> Any:  # type: ignore
        return value
