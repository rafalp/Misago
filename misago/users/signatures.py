from misago.markup import checksums, signature_flavour


def set_user_signature(request, user, signature):
    user.signature = signature

    if signature:
        user.signature_parsed = signature_flavour(request, user, signature)
        user.signature_checksum = make_signature_checksum(user.signature_parsed, user)
    else:
        user.signature_parsed = ''
        user.signature_checksum = ''


def is_user_signature_valid(user):
    if user.signature:
        valid_checksum = make_signature_checksum(user.signature_parsed, user)
        return user.signature_checksum == valid_checksum
    else:
        return False


def make_signature_checksum(parsed_signature, user):
    return checksums.make_checksum(parsed_signature, [user.pk])
