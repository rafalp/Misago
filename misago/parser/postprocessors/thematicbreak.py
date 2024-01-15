from .removerepeats import RemoveRepeatsPostProcessor


class RemoveThematicBreaksRepeatsPostProcessor(RemoveRepeatsPostProcessor):
    checked_types = ["thematic-break-bbcode", "thematic-break"]
