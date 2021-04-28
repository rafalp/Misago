from typing import Any, Dict, List

# Mypy is preventing proper typing for richtext:
# 1. literals are ignored in dict type matching
# 2. recursive types arenunsupported

RichTextBlock = Dict[str, Any]
RichText = List[RichTextBlock]

ParsedMarkupMetadata = dict
