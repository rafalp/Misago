from importlib import import_module

from django.core.exceptions import PermissionDenied
from django.utils import timezone

from misago.conf import settings


class PostingInterrupt(Exception):
    def __init__(self, message):
        if not message:
            raise ValueError("You have to provide PostingInterrupt message.")
        self.message = message


class PostingEndpoint(object):
    START = 0
    REPLY = 1
    EDIT = 2

    def __init__(self, request, mode, **kwargs):
        self.kwargs = kwargs
        self.kwargs.update({'mode': mode, 'request': request, 'user': request.user})

        self.__dict__.update(kwargs)

        # some middlewares (eg. emailnotification) may call render()
        # which will crash if this isn't set to false
        request.include_frontend_context = False

        self.datetime = timezone.now()
        self.errors = {}
        self._is_validated = False

        self.middlewares = self._load_middlewares()
        self._serializers = self._initialize_serializers()

    @property
    def is_start_endpoint(self):
        return self.mode == self.START

    @property
    def is_reply_endpoint(self):
        return self.mode == self.REPLY

    @property
    def is_edit_endpoint(self):
        return self.mode == self.EDIT

    def _load_middlewares(self):
        kwargs = self.kwargs.copy()
        kwargs.update({
            'datetime': self.datetime,
            'parsing_result': {},
        })

        middlewares = []
        for middleware in settings.MISAGO_POSTING_MIDDLEWARES:
            module_name = '.'.join(middleware.split('.')[:-1])
            class_name = middleware.split('.')[-1]

            middleware_module = import_module(module_name)
            middleware_class = getattr(middleware_module, class_name)

            try:
                middleware_obj = middleware_class(prefix=middleware, **kwargs)
                if middleware_obj.use_this_middleware():
                    middlewares.append((middleware, middleware_obj))
            except PostingInterrupt:
                raise ValueError("Posting process can only be interrupted during pre_save phase")

        return middlewares

    def get_serializers(self):
        """return list of serializers belonging to serializerset"""
        return self._serializers

    def _initialize_serializers(self):
        try:
            serializers = {}
            for middleware, obj in self.middlewares:
                serializer = obj.get_serializer()
                if serializer:
                    serializers[middleware] = serializer
            return serializers
        except PostingInterrupt:
            raise ValueError("Posting process can only be interrupted during pre_save phase")

    def is_valid(self):
        """validate data against all serializers"""
        for serializer in self._serializers.values():
            if not serializer.is_valid():
                self.errors.update(serializer.errors)

        self._is_validated = True
        return not self.errors

    def save(self):
        """save new state to backend"""
        if not self._is_validated or self.errors:
            raise RuntimeError("You need to validate posting data successfully before calling save")

        try:
            for middleware, obj in self.middlewares:
                obj.pre_save(self._serializers.get(middleware))
        except PostingInterrupt as e:
            raise ValueError(
                "Posting process can only be interrupted from within interrupt_posting method"
            )

        try:
            for middleware, obj in self.middlewares:
                obj.interrupt_posting(self._serializers.get(middleware))
        except PostingInterrupt as e:
            raise PermissionDenied(e.message)

        try:
            for middleware, obj in self.middlewares:
                obj.save(self._serializers.get(middleware))
            for middleware, obj in self.middlewares:
                obj.post_save(self._serializers.get(middleware))
        except PostingInterrupt as e:
            raise ValueError(
                "Posting process can only be interrupted from within interrupt_posting method"
            )


class PostingMiddleware(object):
    """
    Abstract middleware class
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.__dict__.update(kwargs)

    def use_this_middleware(self):
        return True

    def get_serializer(self):
        pass

    def pre_save(self, serializer):
        pass

    def interrupt_posting(self, serializer):
        pass

    def save(self, serializer):
        pass

    def post_save(self, serializer):
        pass
