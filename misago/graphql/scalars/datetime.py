from datetime import datetime

from ariadne_graphql_modules import ScalarType, gql


class DateTimeScalar(ScalarType):
    __schema__ = gql("scalar DateTime")

    @staticmethod
    def serialize(value: datetime) -> str:  # type: ignore
        return value.isoformat()[:23] + "Z"
