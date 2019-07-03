from social_django.strategy import DjangoStrategy


class MisagoStrategy(DjangoStrategy):
    def setting(self, name, default=None, backend=None):
        if backend:
            backend_settings = self.request.socialauth[backend.name]["settings"]
            if name in backend_settings:
                return backend_settings[name]

        return super().setting(name, default, backend)
