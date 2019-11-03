from ariadne import MutationType
from pydantic import EmailStr, constr, create_model, validate_model, validator

from ...user import create_user


register_mutation = MutationType()


@register_mutation.field("register")
async def resolve_register(_, info, *, input):  # pylint: disable=redefined-builtin
    InputModel = create_registration_model()
    cleaned_data, errors = clean_input_data(input, InputModel)

    if not errors:
        return {
            "user": await create_user(
                cleaned_data["name"],
                cleaned_data["email"],
                password=cleaned_data["password"],
            )
        }

    return {"errors": errors, "user": cleaned_data}


def create_registration_model():
    return create_model(
        "RegisterModel",
        name=(constr(min_length=1, max_length=15, strip_whitespace=True), ...),
        email=EmailStr(),
        password=(constr(min_length=1, max_length=40, strip_whitespace=False), ...),
        __validators__={"password_must_not_be_empty": validate_non_empty_password},
    )


class CustomError(ValueError):
    code = "any_str.empty"


@validator("password")
def validate_non_empty_password(value):
    if not value.strip():
        raise CustomError("password is empty")
    return value


def clean_input_data(input_data, model):
    cleaned_data, _, errors = validate_model(model, input_data)
    return cleaned_data, errors.errors() if errors else []
