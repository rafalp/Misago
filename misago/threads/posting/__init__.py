"""
Posting process implementation
"""
from importlib import import_module

from django.utils import timezone

from misago.conf import settings
from misago.core import forms


START = 0
REPLY = 1
EDIT = 2


class PostingInterrupt(Exception):
    def __init__(self, message):
        if not message:
            raise ValueError("You have to provide PostingInterrupt message.")
        self.message = message


class EditorFormset(object):
    def __init__(self, **kwargs):
        self.errors = []

        self._forms_list = []
        self._forms_dict = {}

        self.kwargs = kwargs
        self.__dict__.update(kwargs)

        self.datetime = timezone.now()

        self.middlewares = []
        self._load_middlewares()

    @property
    def start_form(self):
        return self.mode == START

    @property
    def reply_form(self):
        return self.mode == REPLY

    @property
    def edit_form(self):
        return self.mode == EDIT

    def _load_middlewares(self):
        kwargs = self.kwargs.copy()
        kwargs.update({
            'datetime': self.datetime,
            'parsing_result': {},
        })

        for middleware in settings.MISAGO_POSTING_MIDDLEWARES:
            module_name = '.'.join(middleware.split('.')[:-1])
            class_name = middleware.split('.')[-1]

            middleware_module = import_module(module_name)
            middleware_class = getattr(middleware_module, class_name)

            try:
                middleware_obj = middleware_class(prefix=middleware, **kwargs)
                if middleware_obj.use_this_middleware():
                    self.middlewares.append((middleware, middleware_obj))
            except PostingInterrupt:
                raise ValueError("Posting process can only be "
                                 "interrupted during pre_save phase")

    def get_forms_list(self):
        """return list of forms belonging to formset"""
        if not self._forms_list:
            self._build_forms_cache()
        return self._forms_list

    def get_forms_dict(self):
        """return list of forms belonging to formset"""
        if not self._forms_dict:
            self._build_forms_cache()
        return self._forms_dict

    def _build_forms_cache(self):
        try:
            for middleware, obj in self.middlewares:
                form = obj.make_form()
                if form:
                    self._forms_dict[middleware] = form
                    self._forms_list.append(form)
        except PostingInterrupt:
            raise ValueError("Posting process can only be "
                             "interrupted during pre_save phase")

    def get_main_forms(self):
        """return list of main forms"""
        main_forms = []
        for form in self.get_forms_list():
            try:
                if form.is_main and form.legend:
                    main_forms.append(form)
            except AttributeError:
                pass
        return main_forms

    def get_supporting_forms(self):
        """return list of supporting forms"""
        supporting_forms = {}
        for form in self.get_forms_list():
            try:
                if form.is_supporting:
                    supporting_forms.setdefault(form.location, []).append(form)
            except AttributeError:
                pass
        return supporting_forms

    def is_valid(self):
        """validate all forms"""
        all_forms_valid = True
        for form in self.get_forms_list():
            if not form.is_valid():
                all_forms_valid = False
                for error in form.non_field_errors():
                    self.errors.append(unicode(error))

        return all_forms_valid

    def save(self):
        """change state"""
        forms_dict = self.get_forms_dict()
        for middleware, obj in self.middlewares:
            obj.pre_save(forms_dict.get(middleware))

        try:
            for middleware, obj in self.middlewares:
                obj.save(forms_dict.get(middleware))
            for middleware, obj in self.middlewares:
                obj.post_save(forms_dict.get(middleware))
        except PostingInterrupt as e:
            from misago.threads.posting import floodprotection
            if isinstance(obj, floodprotection.FloodProtectionMiddleware):
                raise e
            else:
                raise ValueError("Posting process can only be "
                                 "interrupted during pre_save phase")

    def update(self):
        """handle POST that shouldn't result in state change"""
        forms_dict = self.get_forms_dict()
        for middleware, obj in self.middlewares:
            obj.pre_save(forms_dict.get(middleware))


class PostingMiddleware(object):
    """
    Abstract middleware classes
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.__dict__.update(kwargs)

    def use_this_middleware(self):
        return True

    def make_form(self):
        pass

    def pre_save(self, form):
        pass

    def save(self, form):
        pass

    def post_save(self, form):
        pass
