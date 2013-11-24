from misago.crawlers import Crawler
from misago import models

class DetectCrawlerMiddleware(object):
    def process_request(self, request):
        # If its correct request (We have client IP), see if it exists in Crawlers DB
        if request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR'):
            found_crawler = Crawler(
                                    request.META.get('HTTP_USER_AGENT', ''),
                                    request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
                                    )
            
            # If crawler exists in database, use it as this request user
            if found_crawler.crawler:
                request.user = models.Crawler(found_crawler.username)