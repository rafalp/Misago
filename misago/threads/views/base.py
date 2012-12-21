class BaseView(object):
    def __new__(cls, request, **kwargs):
        obj = super(BaseView, cls).__new__(cls)
        return obj(request, **kwargs)