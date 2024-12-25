def flood_control(request) -> None:
    if request.user_permissions.exclude_from_flood_control:
        return

    if not request.user.last_posted_on:
        return


def flood_control_last_post(request) -> None:
    pass
