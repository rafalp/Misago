from coffin.template import Library

register = Library()


@register.object(name='intersect')
def intersect(list_a, list_b):
    for i in list_a:
        if i in list_b:
            return True
    return False