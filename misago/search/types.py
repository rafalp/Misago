from dataclasses import dataclass


@dataclass(frozen=True)
class PostSearchResults:
    results: list["PostSearchResult"]
    offset: int
    limit: int
    count: int
    has_more: bool
    time: float

    def __iter__(self):
        yield from self.results


@dataclass(frozen=True)
class PostSearchResult:
    post_id: int
    thread_title: str | None
    post_content: str
    rank: float | None = None
