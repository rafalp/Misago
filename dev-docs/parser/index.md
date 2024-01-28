# Markup parser reference

Misago's markup syntax, parser and renderers that convert parsed markup into an HTML or other representations are implemented in the `misago.parser` package.


## Parsing markup

Parsing markup in Misago is a multi-step process:

1. First, a `ParserContext` instance with parameters for parser functions is created.
2. Next, a `Parser` instance is created that will be used to parse a string into an abstract syntax tree (AST).
3. `Parser` instance is called with a string to parse.
4. The parsed string's AST is walked recursively to create metadata for it.
5. The parsed string's AST, together with it's metadata, is rendered into a desired format: HTML, or one of a few types of plain text.


### Creating `ParserContext`

The `ParserContext` data class is used as a parameter bag for parser functions:

```python
@dataclass(frozen=True)
class ParserContext:
    content_type: str | None
    forum_address: ForumAddress
    request: HttpRequest | None
    user: User | AnonymousUser
    user_permissions: UserPermissionsProxy
    settings: DynamicSettings
    cache_versions: dict
    plugin_data: dict
```

While you can instantiate the `ParserContext` class yourself, doing so prevents plugins from including their own data in it. Instead, you should use the dedicated factory function, `create_parser_context`:

```python
from misago.parser.context import create_parser_context
```

If you have Django's `request` object at hand, you can create the context from it:

```python
from misago.parser.context import create_parser_context

context = create_parser_context(request)
```

In other situations (eg. in management commands and Celery taks) you will have to create it yourself:

```python
from django.contrib.auth.models import AnonymousUser
from misago.cache.versions import get_cache_versions
from misago.conf.dynamicsettings import DynamicSettings
from misago.parser.context import create_parser_context
from misago.permissions.proxy import UserPermissionsProxy

cache_versions = get_cache_versions()
dynamic_settings = DynamicSettings(cache_versions)

context = create_parser_context(
    user_permissions=UserPermissionsProxy(AnonymousUser(), cache_versions),
    cache_versions=cache_versions,
    settings=dynamic_settings,
)
```

You can tell the parser what type of content is it parsing by setting the `content_type` option:

```python
from misago.parser.context import create_parser_context

context = create_parser_context(
    ...,
    content_type="USER_SIGNATURE",
)
```

Context object also includes the `plugin_data` dict with additional context added by the plugins, and the `ForumAddress` utility that can be used to test if a link is an inbound link:

```python
inbound_link = context.forum_address.is_inbound_link("https://example.com")
```


### Creating and using `Parser` instance

Once you have an instance of `ParserContext`, you can use the `create_parser` factory function to create a parser instance:

```python
from misago.parser.factory import create_parser_context

parse = create_parser(context)
```

Similar to the context, you can instantiate the `Parser` class directly. However, doing so will create an empty `Parser` instance that doesn't support parsing any syntax and will exclude any plugins.

`Parser` is a callable class. To parse a markup into AST, use the `Parser` instance like a function:

```python
ast = parse("Hello *World*!")
```

`Parser` parses markup in three stages:

- Blocks
- Inline syntax
- Post-processors


### Creating AST metadata

Once the markup string has been parsed, and its abstract syntax tree representation is available, the `create_ast_metadata` function should be used to retrieve metadata from it:"

```python
from misago.parser.metadata import create_ast_metadata

metadata = create_ast_metadata(context, ast)
```

The `metadata` is a `dict` that contains additional data about the `ast`. For example, if original markup included any `@mention`s of existing users, those users instances will be available through metadata's `users` key.


### Rendering AST into a target format

Abstract syntax tree representation of parsed markup can be rendered into one of two formats:

- HTML
- Plain text

HTML format is used for rendering content on the site, while plain text is useful for `meta` description tags and search documents.

To render AST to HTML, use the `render_ast_to_html` function:

```python
from misago.parser.html import render_ast_to_html

html = render_ast_to_html(context, ast, metadata)
```

To produce a plain text instead, use the `render_ast_to_plaintext` instead:

```python
from misago.parser.plaintext import render_ast_to_plaintext

text = render_ast_to_plaintext(context, ast, metadata)
```

Because there are multiple uses for "plain text", you can specify the target format:

```python
from misago.parser.plaintext import PlainTextFormat, render_ast_to_plaintext

text = render_ast_to_plaintext(
    context, ast, metadata, text_format=PlainTextFormat.SEARCH_DOCUMENT
)
```


### Complete example

Below code implements a function that abstracts away the entire setup process:

```python
from django.http import HttpRequest
from misago.parser.context import create_parser_context
from misago.parser.factory import create_parser
from misago.parser.html import render_ast_to_html
from misago.parser.metadata import create_ast_metadata


def parse_str_to_html(request: HttpRequest, markup: str) -> str:
    context = create_parser_context(request)
    parse = create_parser(context)
    ast = parse(markup)
    metadata = create_ast_metadata(context, ast)
    return render_ast_to_html(context, ast, metadata)
```


## Abstract Syntax Tree

Parsed markup is represented as an abstract syntax tree. This three is a `list` of `dict`s.

For example, this markup:

```markdown
Hello world! How's *going*?
```

Is parsed to the following AST:

```json
[
    {
        "type": "paragraph",
        "children": [
            {
                "type": "text",
                "text": "Hello world! How's "
            },
            {
                "type": "emphasis",
                "children": [
                    {
                        "type": "text",
                        "text": "going"
                    }
                ]
            },
            {
                "type": "text",
                "text": "Hello world! How's "
            }
        ]
    }
]
```

Misago's markup AST reference is available [here](./ast.md).
