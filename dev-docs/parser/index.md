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