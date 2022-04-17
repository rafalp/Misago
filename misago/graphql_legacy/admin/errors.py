class MisagoGraphQLError(Exception):
    extensions = {
        "code": "ERROR",
    }


class AuthenticationGraphQLError(MisagoGraphQLError):
    message = "Authentication is required."
    extensions = {
        "code": "UNAUTHENTICATED",
    }


class ForbiddenGraphQLError(MisagoGraphQLError):
    message = "Admin status is required."
    extensions = {
        "code": "FORBIDDEN",
    }
