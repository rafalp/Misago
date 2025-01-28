from ...core.utils import slugify
from ..parser import Parser, Pattern
from .urls import ImgBBCode, ImgMarkdown, UrlBBCode, UrlMarkdown


class AttachmentMarkdown(Pattern):
    pattern_type: str = "attachment"
    pattern: str = r"\<attachment=.+?\>\s*"
    invalid_parents: set[str] = {
        ImgBBCode.pattern_type,
        ImgMarkdown.pattern_type,
        UrlMarkdown.pattern_type,
        UrlBBCode.pattern_type,
    }

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> dict:
        args = [a.strip() for a in match.strip()[12:-1].strip('" ').split(":")]

        if len(args) != 2:
            return {"type": "text", "text": match}

        name, attachment_id = args
        try:
            attachment_id = int(attachment_id)
        except (ValueError, TypeError):
            return {"type": "text", "text": match}

        if not name or attachment_id < 1:
            return {"type": "text", "text": match}

        return {
            "type": self.pattern_type,
            "name": name,
            "slug": slugify(name),
            "id": attachment_id,
        }
