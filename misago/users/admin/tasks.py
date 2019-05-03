from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def delete_user_with_content(pk):
    try:
        user = User.objects.get(pk=pk, is_staff=False, is_superuser=False)
    except User.DoesNotExist:
        pass
    else:
        user.delete(delete_content=True)
