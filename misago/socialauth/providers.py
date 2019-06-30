class Providers:
    def __init__(self):
        self._dict = {}
        self._list = []

    def dict(self):
        return self._dict

    def list(self):
        return self._list

    def is_registered(self, provider):
        return provider in self._dict

    def add(
        self, *, provider, name, auth_backend, settings=None, admin_form, admin_template
    ):
        data = {
            "provider": provider,
            "name": name,
            "auth_backend": auth_backend,
            "settings": settings or {},
            "admin_form": admin_form,
            "admin_template": admin_template,
        }

        self._dict[provider] = data
        self._list.append(data)
        self._list = sorted(self._list, key=lambda k: k["name"])

    def get_name(self, provider):
        return self._dict.get(provider)["name"]

    def get_auth_backend(self, provider):
        return self._dict.get(provider)["auth_backend"]

    def get_settings(self, provider):
        return self._dict.get(provider)["settings"]

    def get_admin_form_class(self, provider):
        return self._dict.get(provider)["admin_form"]

    def get_admin_template_name(self, provider):
        return self._dict.get(provider)["admin_template"]


providers = Providers()
