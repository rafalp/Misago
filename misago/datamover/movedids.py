def get(model, id):
    from .models import MovedId
    try:
        return MovedId.objects.get(model=model, old_id=id).new_id
    except MovedId.DoesNotExist:
        return None


def set(model, old_id, new_id):
    from .models import MovedId
    MovedId.objects.create(
        model=model,
        old_id=old_id,
        new_id=new_id,
    )
