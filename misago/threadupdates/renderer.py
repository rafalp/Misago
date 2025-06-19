from typing import TYPE_CHECKING

from .models import ThreadUpdate

if TYPE_CHECKING:
    from .actions import ThreadUpdateAction


class ThreadUpdatesRenderer:
    actions: dict[str, "ThreadUpdateAction"]

    def __init__(self):
        self.actions = {}

    def register_action(self, action: type["ThreadUpdateAction"]):
        action_obj = action()
        self.actions[action_obj.action] = action_obj
        return action

    def render_thread_update(
        self, thread_update: ThreadUpdate, data: dict
    ) -> dict | None:
        action = self.actions.get(thread_update.action)
        if not action:
            return

        return {
            "icon": action.icon,
            "description": action.get_description(thread_update, data),
        }


thread_updates_renderer = ThreadUpdatesRenderer()
