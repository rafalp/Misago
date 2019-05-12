from .forms import get_permissions_forms


def mock_role_form_data(model, data):
    """
    In order for form to don't fail submission, all permission fields need
    to receive values. This function populates data dict with default values
    for permissions, making form validation pass
    """
    for form in get_permissions_forms(model):
        for field in form:
            if field.value() is True:
                data[field.html_name] = 1
            elif field.value() is False:
                data[field.html_name] = 0
            else:
                data[field.html_name] = field.value()
    return data
