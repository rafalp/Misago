from pydantic.errors import PydanticErrorMixin, PydanticTypeError, PydanticValueError


class BaseError(PydanticErrorMixin, Exception):
    pass


VALIDATION_ERRORS = (BaseError, PydanticValueError, PydanticTypeError)


class AllFieldsAreRequiredError(PydanticValueError):
    code = "all_fields_are_required"
    msg_template = "all fields are required"


class ListRepeatedItemsError(PydanticValueError):
    code = "list.repeated_items"
    msg_template = "ensure all items of the list are unique"


class SiteWizardDisabledError(PydanticValueError):
    code = "site_wizard.disabled"
    msg_template = "site wizard is disabled"
