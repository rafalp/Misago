from django.utils import timezone
from misago.monitor.models import Item

def load_monitor_fixture(fixture):
    for id in fixture.keys():
        item = Item(
                    id=id,
                    value=fixture[id],
                    updated=timezone.now()
                    )
        item.save(force_insert=True)
