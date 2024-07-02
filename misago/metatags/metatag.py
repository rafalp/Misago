import html
from dataclasses import dataclass


@dataclass(frozen=True)
class MetaTag:
    content: str | int
    name: str | None = None
    property: str | None = None
    itemprop: str | None = None

    def get_attrs(self) -> dict[str, str]:
        attrs: dict[str, str] = {}
        if self.name:
            attrs["name"] = str(self.name)
        if self.property:
            attrs["property"] = str(self.property)
        if self.itemprop:
            attrs["itemprop"] = str(self.itemprop)
        attrs["content"] = str(self.content)
        return attrs

    def as_html(self):
        attrs: dict[str, str] = self.get_attrs()

        attrs_html = [f'{name}="{html.escape(value)}"' for name, value in attrs.items()]
        return f"<meta {' '.join(attrs_html)}>"
