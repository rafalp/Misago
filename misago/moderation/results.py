from dataclasses import dataclass


class ModerationResult:
    pass


@dataclass(frozen=True)
class ModerationTemplateResult:
    context: dict
    template_name: str

    def update_context(self, context: dict):
        self.context.update(context)


class ModerationBulkResult:
    updated: set[int]

    def __init__(self, updated: set[int]):
        self.updated = updated
