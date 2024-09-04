from ..paginator import ThreadRepliesPaginator
from ..test import reply_thread


def test_thread_replies_paginator_counts_pages_without_orphans(thread):
    paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
    assert paginator.count == 1
    assert paginator.num_pages == 1

    # Fill in first page
    for i in range(4):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
        assert paginator.count == 2 + i
        assert paginator.num_pages == 1

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
    assert paginator.count == 5
    assert paginator.num_pages == 1

    # Fill in second page
    for i in range(5):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
        assert paginator.count == 6 + i
        assert paginator.num_pages == 2

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
    assert paginator.count == 10
    assert paginator.num_pages == 2

    # Fill in third page
    for i in range(5):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
        assert paginator.count == 11 + i
        assert paginator.num_pages == 3

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
    assert paginator.count == 15
    assert paginator.num_pages == 3


def test_thread_replies_paginator_counts_pages_with_orphans(thread):
    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 1
    assert paginator.num_pages == 1

    # Fill in first page
    for i in range(4):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
        assert paginator.count == 2 + i
        assert paginator.num_pages == 1

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 5
    assert paginator.num_pages == 1

    # Add orphans
    for i in range(2):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
        assert paginator.count == 6 + i
        assert paginator.num_pages == 1

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 7
    assert paginator.num_pages == 1

    # Orphans + 1 produces new page
    reply_thread(thread)
    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 8
    assert paginator.num_pages == 2

    # Fill in second page
    for i in range(2):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
        assert paginator.count == 9 + i
        assert paginator.num_pages == 2

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 10
    assert paginator.num_pages == 2

    # Add orphans
    for i in range(2):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
        assert paginator.count == 11 + i
        assert paginator.num_pages == 2

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 12
    assert paginator.num_pages == 2

    # Orphans + 1 produces new page
    reply_thread(thread)
    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 13
    assert paginator.num_pages == 3


def test_thread_replies_paginator_without_orphans_calculates_item_page(thread):
    paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)

    # First item page
    assert paginator.get_item_page(0) == 1

    # First page items
    for i in range(4):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
        assert paginator.get_item_page(i) == 1

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
    assert paginator.count == 5
    assert paginator.num_pages == 1

    # Second page items
    for i in range(5):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
        assert paginator.get_item_page(5 + i) == 2

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
    assert paginator.count == 10
    assert paginator.num_pages == 2

    # Third page items
    for i in range(5):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
        assert paginator.get_item_page(10 + i) == 3

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
    assert paginator.count == 15
    assert paginator.num_pages == 3


def test_thread_replies_paginator_with_orphans_calculates_item_page(thread):
    paginator = ThreadRepliesPaginator(thread.post_set, 5, 3)

    # First item page
    assert paginator.get_item_page(0) == 1

    # First page items
    for i in range(4):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
        assert paginator.get_item_page(i) == 1

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 0)
    assert paginator.count == 5
    assert paginator.num_pages == 1

    # Add orphans
    for i in range(2):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
        assert paginator.get_item_page(i) == 1

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 7
    assert paginator.num_pages == 1

    # Orphans + 1 produces second page
    reply_thread(thread)
    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 8
    assert paginator.num_pages == 2

    # Item offsets changed when orphans were moved to second page
    for i in range(8):
        if i < 5:
            assert paginator.get_item_page(i) == 1
        else:
            assert paginator.get_item_page(i) == 2

    # Fill in second page items
    for i in range(2):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
        assert paginator.get_item_page(9 + i) == 2

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 10
    assert paginator.num_pages == 2

    # Add orphans to second page
    for i in range(2):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
        assert paginator.get_item_page(11 + i) == 2

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 12
    assert paginator.num_pages == 2

    # Orphans + 1 produces third page
    reply_thread(thread)
    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 13
    assert paginator.num_pages == 3

    for i in range(13):
        if i < 5:
            assert paginator.get_item_page(i) == 1
        elif i < 10:
            assert paginator.get_item_page(i) == 2
        else:
            assert paginator.get_item_page(i) == 3

    # Fill in third page
    for i in range(2):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
        assert paginator.get_item_page(14 + i) == 3

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 15
    assert paginator.num_pages == 3

    # Add orphans to third page
    for i in range(2):
        reply_thread(thread)
        paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
        assert paginator.get_item_page(16 + i) == 3

    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 17
    assert paginator.num_pages == 3

    for i in range(17):
        if i < 5:
            assert paginator.get_item_page(i) == 1
        elif i < 10:
            assert paginator.get_item_page(i) == 2
        else:
            assert paginator.get_item_page(i) == 3

    # Orphans + 1 produces four page
    reply_thread(thread)
    paginator = ThreadRepliesPaginator(thread.post_set, 5, 2)
    assert paginator.count == 18
    assert paginator.num_pages == 4

    for i in range(18):
        if i < 5:
            assert paginator.get_item_page(i) == 1
        elif i < 10:
            assert paginator.get_item_page(i) == 2
        elif i < 15:
            assert paginator.get_item_page(i) == 3
        else:
            assert paginator.get_item_page(i) == 4
