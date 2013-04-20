import math
from django.http import Http404

def make_pagination(page, total, per):
    pagination = {'start': 0, 'stop': 0, 'prev':-1, 'next':-1}
    page = int(page)

    if page == 1:
        # This is fugly abuse of "wrong page" handling
        # It's done to combat "duplicate content" errors
        # If page is 1 instead of 0, that suggests user came
        # to page from somewhere/1/ instead of somewhere/
        # when this happens We raise 404 to drop /1/ part from url
        raise Http404()

    if page > 0:
        pagination['start'] = (page - 1) * per

    # Set page and total stat
    pagination['page'] = int(pagination['start'] / per) + 1
    pagination['total'] = int(math.ceil(total / float(per)))

    # Fix too large offset
    if pagination['start'] > total:
        pagination['start'] = 0

    # Allow prev/next?
    if total > per:
        if pagination['page'] > 1:
            pagination['prev'] = pagination['page'] - 1
        if pagination['page'] < pagination['total']:
            pagination['next'] = pagination['page'] + 1

    # Fix empty pagers
    if not pagination['total']:
        pagination['total'] = 1

    # Set stop offset
    pagination['stop'] = pagination['start'] + per

    # Put 1/5 of last page on current page...
    if pagination['page'] + 1 == pagination['total']:
        last_page = per + total - (pagination['total'] * per)
        cutoff = int(per / 5)
        if cutoff > 1 and last_page < cutoff:
            pagination['stop'] += last_page
            pagination['total'] -= 1
            pagination['next'] = -1

    # Raise 404 if page is out of range
    if pagination['page'] > pagination['total']:
        raise Http404()

    # Return complete pager
    return pagination


def page_number(item, total, per):
    page_item = int(item / per) + 1
    pages_total = int(math.ceil(total / float(per)))
    if page_item == pages_total and total - (total * pages_total) < int(per / 5):
        page_item -= 1
    return page_item