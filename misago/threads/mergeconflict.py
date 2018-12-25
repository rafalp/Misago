from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from .models import Poll


class MergeConflictHandler:
    def __init__(self, threads):
        self.items = []
        self.choices = {0: None}

        self._is_valid = False
        self._resolution = None

        self.threads = threads
        self.populate_from_threads(threads)

        if len(self.items) == 1:
            self._is_valid = True
            self._resolution = self.items[0]

    def populate_from_threads(self, threads):
        raise NotImplementedError("merge handler must define populate_from_threads")

    def is_merge_conflict(self):
        return len(self.items) > 1

    def set_resolution(self, resolution):
        try:
            resolution_clean = int(resolution)
        except (TypeError, ValueError):
            return

        if resolution_clean in self.choices:
            self._resolution = self.choices[resolution_clean]
            self._is_valid = True

    def is_valid(self):
        return self._is_valid

    def get_resolution(self):
        return self._resolution or None


class BestAnswerMergeHandler(MergeConflictHandler):
    data_name = "best_answer"

    def populate_from_threads(self, threads):
        for thread in threads:
            if thread.has_best_answer:
                self.items.append(thread)
                self.choices[thread.pk] = thread
        self.items.sort(key=lambda thread: (thread.title, thread.id))

    def get_available_resolutions(self):
        resolutions = [[0, _("Unmark all best answers")]]
        for thread in self.items:
            resolutions.append([thread.pk, thread.title])
        return resolutions


class PollMergeHandler(MergeConflictHandler):
    data_name = "poll"

    def populate_from_threads(self, threads):
        for thread in threads:
            try:
                self.items.append(thread.poll)
                self.choices[thread.poll.id] = thread.poll
            except Poll.DoesNotExist:
                pass
        self.items.sort(key=lambda poll: poll.question)

    def get_available_resolutions(self):
        resolutions = [[0, _("Delete all polls")]]
        for poll in self.items:
            resolutions.append(
                [poll.id, "%s (%s)" % (poll.question, poll.thread.title)]
            )
        return resolutions


class MergeConflict:
    """
    Utility class single point of entry for detecting merge conflicts on different
    properties and validating user resolutions.
    """

    HANDLERS = (BestAnswerMergeHandler, PollMergeHandler)

    def __init__(self, data=None, threads=None):
        self.data = data or {}
        self._handlers = [Handler(threads) for Handler in self.HANDLERS]
        self._conflicts = [i for i in self._handlers if i.is_merge_conflict()]
        self.set_resolution(data)

    def is_merge_conflict(self):
        return bool(self._conflicts)

    def get_conflicting_fields(self):
        return [i.data_name for i in self._conflicts]

    def set_resolution(self, data):
        for handler in self._conflicts:
            data = self.data.get(handler.data_name)
            handler.set_resolution(data)

    def is_valid(self, raise_exception=False):
        if raise_exception:
            self.raise_exception()
        return all([i.is_valid() for i in self._handlers])

    def raise_exception(self):
        # if any choice was made by user, we are in validation stage of resolution
        for conflict in self._conflicts:
            if self.data.get(conflict.data_name) is not None:
                self.raise_validation_exception()
                break
        else:
            self.raise_resolutions_exception()

    def raise_validation_exception(self):
        errors = {}
        for conflict in self._conflicts:
            if not conflict.is_valid() or self.data.get(conflict.data_name) is None:
                errors[conflict.data_name] = [_("Invalid choice.")]
        if errors:
            raise ValidationError(errors)

    def raise_resolutions_exception(self):
        resolutions = {}
        for conflict in self._conflicts:
            key = "%ss" % conflict.data_name
            resolutions[key] = conflict.get_available_resolutions()
        if resolutions:
            raise ValidationError(resolutions)

    def get_resolution(self):
        resolved_handlers = [i for i in self._handlers if i.is_valid()]
        return {i.data_name: i.get_resolution() for i in resolved_handlers}
