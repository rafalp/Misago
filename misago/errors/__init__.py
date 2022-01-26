from typing import Union

from pydantic import PydanticValueError

from .errordict import ErrorDict
from .errorslist import ErrorsList
from .format import get_error_dict, get_error_location, get_error_type


class AllFieldsAreRequiredError(PydanticValueError):
    code = "all_fields_are_required"
    msg_template = "all fields are required"


class ListRepeatedItemsError(PydanticValueError):
    code = "list.repeated_items"
    msg_template = "ensure all items of the list are unique"


class SiteWizardDisabledError(PydanticValueError):
    code = "site_wizard.disabled"
    msg_template = "site wizard is disabled"
