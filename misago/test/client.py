from django.test import Client


class MisagoClient(Client):
    def post(self, *args, **kwargs):
        if "json" in kwargs:
            return super().post(
                *args,
                data=kwargs.pop("json"),
                content_type="application/json",
                **kwargs,
            )

        return super().post(*args, **kwargs)

    def put(self, *args, **kwargs):
        if "json" in kwargs:
            return super().put(
                *args,
                data=kwargs.pop("json"),
                content_type="application/json",
                **kwargs,
            )

        return super().put(*args, **kwargs)
