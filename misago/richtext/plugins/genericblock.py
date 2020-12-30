from functools import wraps


def parse_generic_block_open(f):
    @wraps(f)
    def wrapped_parse_generic_block_open(parser, m, *args):
        block = f(parser, m, *args)
        return "block_open", block, m.group(0)

    return wrapped_parse_generic_block_open


def parse_generic_block_close(f):
    @wraps(f)
    def wrapped_parse_generic_block_close(parser, m, *args):
        block = f(parser, m, *args)
        return "block_close", block, m.group(0)

    return wrapped_parse_generic_block_close


def plugin_generic_block(markdown):
    if markdown.renderer.NAME == "ast":
        markdown.renderer.register("block_open", render_ast_block_open)
        markdown.renderer.register("block_close", render_ast_block_close)


def render_ast_block_open(block, fallback):
    return {
        "type": "block_open",
        "block_type": block["type"],
        "ast": block,
        "fallback": fallback,
    }


def render_ast_block_close(block, fallback):
    return {"type": "block_close", "block_type": block["type"], "fallback": fallback}
