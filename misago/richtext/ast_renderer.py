from mistune import AstRenderer


class MisagoAstRenderer(AstRenderer):
    def paragraph(self, children):
        return {"type": "p", "children": children}
