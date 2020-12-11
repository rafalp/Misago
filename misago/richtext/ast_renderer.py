from mistune import AstRenderer
from ..utils.strings import get_random_string


class MisagoAstRenderer(AstRenderer):
    list2_elements = tuple()

    def paragraph(self, children):
        return {"children": children, "id": get_random_string(), "type": "p"}

    def quote(self, parsed_data):
        children = parsed_data["children"]
        return {
            "author": parsed_data.get("author"),
            "children": children,
            "type": "quote",
        }

    def color(self, parsed_data):
        children = parsed_data["children"]
        return {
            "color": parsed_data.get("color"),
            "children": children,
            "type": "color",
        }

    def size(self, parsed_data):
        children = parsed_data["children"]
        return {"size": parsed_data.get("size"), "children": children, "type": "size"}

    def link2(self, parsed_data):
        parsed_data["type"] = "link"
        return parsed_data

    def list_start(self, parsed_data):
        self.list2_elements = []
        return {"type": "list", "children": self.list2_elements}

    def list_end(self, parsed_data):
        return None

    def list2_item(self, parsed_data):
        element = {"type": "list_element", "children": parsed_data}
        self.list2_elements.append(element)
        return None

    def image2(self, parsed_data):
        parsed_data["type"] = "image"
        return parsed_data
