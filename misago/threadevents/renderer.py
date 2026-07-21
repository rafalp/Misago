from typing import TYPE_CHECKING

from .models import ThreadEvent

if TYPE_CHECKING:
    from .actions import ThreadUpdateAction


class ThreadEventsRenderer:
    actions: dict[str, "ThreadUpdateAction"]

    def __init__(self):
        self.actions = {}

    def register_action(self, action: type["ThreadUpdateAction"]):
        action_obj = action()
        self.actions[action_obj.action] = action_obj
        return action

    def render_thread_event(self, thread_event: ThreadEvent, data: dict) -> dict | None:
        action = self.actions.get(thread_event.action)
        if not action:
            return

        return {
            "icon": action.icon,
            "description": action.get_description(thread_event, data),
        }


thread_events_renderer = ThreadEventsRenderer()
