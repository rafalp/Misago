from typing import TYPE_CHECKING

from .models import ThreadEvent

if TYPE_CHECKING:
    from .types import ThreadEventType


class ThreadEventsRenderer:
    event_types: dict[str, "ThreadEventType"]

    def __init__(self):
        self.event_types = {}

    def register_thread_event_type(
        self, thread_event_type_cls: type["ThreadEventType"]
    ):
        thread_event_type = thread_event_type_cls()
        self.event_types[thread_event_type.event_type] = thread_event_type
        return thread_event_type_cls

    def render_thread_event(self, thread_event: ThreadEvent, data: dict) -> dict | None:
        event_type = self.event_types.get(thread_event.event_type)
        if not event_type:
            return

        return {
            "icon": event_type.icon,
            "description": event_type.get_description(thread_event, data),
        }


thread_events_renderer = ThreadEventsRenderer()
