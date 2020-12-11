from mistune import HTMLRenderer


class MisagoHTMLRenderer(HTMLRenderer):
    def underline(self, text):
        return f'<span style="text-decoration: underline">{text}</span>'

    def line_through(self, text):
        return f'<span style="text-decoration: line-through">{text}</span>'

    def center(self, text):
        return f"<center>{text}</center>"

    def quote(self, data):
        return f'<quote author="{data["author"]}">{data["children"]}</quote>'

    def color(self, data):
        return f'<span style="color: {data["color"]}">{data["children"]}</span>'

    def size(self, data):
        return f'<span style="font-size: {data["size"]}px">{data["children"]}</span>'

    def link2(self, data):
        return f'<a href="{data["link"]}" title="{data["title"]}">{data["title"]}</a>'

    def list_start(self, data):
        return "<ul>"

    def list_end(self, data):
        return "</ul>"

    def list2_item(self, data):
        return super().list_item(data, 0)

    def image2(self, data):
        return f'<img src="{data["src"]}" alt="{data["alt"]}" title="{data["title"]}">'
