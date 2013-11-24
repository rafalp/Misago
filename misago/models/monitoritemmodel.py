from django.db import models

class MonitorItem(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    _value = models.TextField(db_column="value", blank=True, null=True)
    type = models.CharField(max_length=255, default="int")
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'misago'

    @property
    def value(self):
        if self.type in ("int", "integer"):
            return int(self._value)
        if self.type == "float":
            return float(self._value)
        return self._value

    @value.setter
    def value(self, v):
        if self.type in ("int", "integer"):
            self._value = int(v)
        if self.type == "float":
            self._value = float(v)
        self._value = v
