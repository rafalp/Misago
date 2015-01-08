from misago.markup import parse

from misago.threads.checksums import update_report_checksum
from misago.threads.models import Report


def make_posts_reports_aware(user, thread, posts):
    make_posts_aware = (
        user.is_authenticated() and
        thread.has_reported_posts and
        thread.acl['can_report']
    )

    if not make_posts_aware:
        return

    posts_dict = {}
    for post in posts:
        post.is_reported = False
        post.report = None
        posts_dict[post.pk] = post

    for report in user.report_set.filter(post_id__in=posts_dict.keys()):
        posts_dict[report.post_id].is_reported = True
        posts_dict[report.post_id].report = report


def user_has_reported_post(user, post):
    if not post.has_reports:
        return False

    return post.report_set.filter(reported_by=user).exists()


def report_post(request, post, message):
    if message:
        message = parse(message, request, request.user,
                        allow_images=False, allow_blocks=False)
        message = message['parsed_text']

    report = Report.objects.create(
        forum=post.forum,
        thread=post.thread,
        post=post,
        reported_by=request.user,
        reported_by_name=request.user.username,
        reported_by_slug=request.user.slug,
        reported_by_ip=request.user.ip,
        message=message,
        checksum=''
    )

    if message:
        update_report_checksum(report)
        report.save(update_fields=['checksum'])

    post.thread.has_reported_posts = True
    post.thread.has_open_reports = True
    post.thread.save(update_fields=['has_reported_posts', 'has_open_reports'])

    post.has_reports = True
    post.has_open_reports = True
    post.save(update_fields=['has_reports', 'has_open_reports'])

    return report
