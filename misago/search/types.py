from dataclasses import dataclass


@dataclass(frozen=True)
class ThreadsSearchResults:
    results: list["ThreadsSearchResultItem"]
    has_more: bool
    time: float

    def __iter__(self):
        yield from self.results


@dataclass(frozen=True)
class ThreadsSearchResultItem:
    post_id: int
    thread_title: str
    post_content: str
    rank: float | None = None
