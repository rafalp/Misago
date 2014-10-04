from misago.markup import checksums


def is_valid(notification):
    valid_checksum = make_checksum(notification)
    return notification.checksum == valid_checksum


def make_checksum(notification):
    checksum_seeds = [unicode(notification.id), unicode(notification.user_id)]
    return checksums.make_checksum(notification.message, checksum_seeds)


def update_checksum(notification):
    notification.checksum = make_checksum(notification)
    return notification.checksum
