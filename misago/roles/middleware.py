class ACLMiddleware(object):
    def process_request(self, request):
        print 'ACL MIDDLEWARE!!!'