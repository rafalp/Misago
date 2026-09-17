from dataclasses import dataclass


@dataclass(frozen=True)
class ThreadsSearchResult:
    items: list["ThreadsSearchResultItem"]
    has_more: bool
    time: float

    def __iter__(self):
        yield from self.items


@dataclass(frozen=True)
class ThreadsSearchResultItem:
    post_id: int
    thread_title: str
    post_content: str
    rank: float | None = None
