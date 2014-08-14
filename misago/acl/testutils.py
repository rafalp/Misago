from hashlib import md5
from time import time

from misago.core import threadstore

from misago.acl.forms import get_permissions_forms
from misago.acl.models import Role


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
    """overrides user permissions with specified ones"""
    final_cache = user.acl
    final_cache.update(new_acl)

    user._acl_cache = final_cache
    user.acl_key = md5(unicode(user.pk)).hexdigest()[:8]
    user.save()

    threadstore.set('acl_%s' % user.acl_key, final_cache)
