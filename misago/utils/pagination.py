import math

def make_pagination(page, total, max):
    pagination = {'start': 0, 'stop': 0, 'prev':-1, 'next':-1}
    page = int(page)
    if page > 0:
        pagination['start'] = (page - 1) * max

    # Set page and total stat
    pagination['page'] = int(pagination['start'] / max) + 1
    pagination['total'] = int(math.ceil(total / float(max)))

    # Fix too large offset
    if pagination['start'] > total:
        pagination['start'] = 0

    # Allow prev/next?
    if total > max:
        if pagination['page'] > 1:
            pagination['prev'] = pagination['page'] - 1
        if pagination['page'] < pagination['total']:
            pagination['next'] = pagination['page'] + 1

    # Fix empty pagers
    if not pagination['total']:
        pagination['total'] = 1

    # Set stop offset
    pagination['stop'] = pagination['start'] + max
    return pagination
