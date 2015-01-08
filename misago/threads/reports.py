from misago.markup import parse

from misago.threads.checksums import update_report_checksum
from misago.threads.models import Report


def user_has_reported_post(user, post):
    if not post.has_reports:
        return False

    # todo: do exists in the post reports set

def report_post(request, post, message):
    if message:
        message = parse(message, request, request.user)['parsed_text']

    report = Report.objects.create(
        forum=post.forum,
        thread=post.thread,
        post=post,
        reported_by=post.user,
        reported_by_name=post.user.username,
        reported_by_slug=post.user.slug,
        reported_by_ip=post.user.ip,
        message=message,
        checksum=''
    )

    if message:
        update_report_checksum(report.checksum)
        report.save(update_fields=['checksum'])

    post.thread.has_reported_posts = True
    post.thread.has_open_reports = True
    post.thread.save(update_fields=['has_reported_posts', 'has_open_reports'])

    post.has_reports = True
    post.has_open_reports = True
    post.thread.save(update_fields=['has_reports', 'has_open_reports'])

    return report
