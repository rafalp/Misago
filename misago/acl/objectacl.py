from .providers import providers


def add_acl_to_obj(user_acl, obj):
    """add valid ACL to obj (iterable of objects or single object)"""
    if hasattr(obj, "__iter__"):
        for item in obj:
            _add_acl_to_obj(user_acl, item)
    else:
        _add_acl_to_obj(user_acl, obj)


def _add_acl_to_obj(user_acl, obj):
    """add valid ACL to single obj, helper for add_acl function"""
    obj.acl = {}

    for annotator in providers.get_obj_type_annotators(obj):
        annotator(user_acl, obj)
