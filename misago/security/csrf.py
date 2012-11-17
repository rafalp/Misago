from django import forms

class CSRFProtection(object):
    def __init__(self, csrf_token):
        self.csrf_id = '_csrf_token'
        self.csrf_token = csrf_token
        
    def request_secure(self, request):
        return request.method == 'POST' and request.POST.get(self.csrf_id) == self.csrf_token