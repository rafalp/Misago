import math

def make_pagination(page, total, per):
    pagination = {'start': 0, 'stop': 0, 'prev':-1, 'next':-1}
    page = int(page)
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

    # Return complete pager
    return pagination
