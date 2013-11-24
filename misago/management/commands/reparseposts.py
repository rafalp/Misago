from django.core.management.base import BaseCommand
from misago.markdown import post_markdown
from misago.models import Post

class Command(BaseCommand):
    help = 'Reparse markdown for all forum posts'

    def handle(self, *args, **options):
        count = 0
        total = Post.objects.count()
        last = 0

        self.stdout.write('\nReparsing posts...')
        for post in Post.objects.iterator():
            md, post.post_preparsed = post_markdown(post.post)
            post.save(force_update=True)
            count += 1
            progress = (count * 100 / total)
            if not progress % 10 and progress > last and progress < 100:
                self.stdout.write('Reparsed %s out of %s posts...' % (count, total))
                last = progress
        self.stdout.write('\n%s posts have been reparsed.\n' % count)
