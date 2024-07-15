from django import forms
from django.http import HttpRequest

from ..threads.models import Thread


class MergeThreads(forms.Form):
    threads: list[Thread]
    request: HttpRequest

    title = forms.CharField(label="THREAD TITLE")

    def __init__(
        self,
        data: dict | None=None,
        *,
        threads: list[Thread],
        request: HttpRequest,
    ):
        super().__init__(data)

        self.threads = threads
        self.request = request
