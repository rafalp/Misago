from misago.acl.forms import get_permissions_forms


def fake_post_data(target, data_dict):
    """
    In order for form to don't fail submission, all permission fields need
    to receive values. This function populates data dict with default values
    for permissions, making form validation pass
    """
    for form in get_permissions_forms(target):
        for field in form:
            if field.value() == True:
                data_dict[field.html_name] = 1
            elif field.value() == False:
                data_dict[field.html_name] = 0
            else:
                data_dict[field.html_name] = field.value()
    return data_dict


def override_acl(user, new_acl):
    user.acl
    user._acl_cache.update(new_acl)
