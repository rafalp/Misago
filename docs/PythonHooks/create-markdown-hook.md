# `create_markdown_hook`

```python
create_post_hook.call_action(
    action: CreateMarkdownAction,
    context: GraphQLContext,
    block: BlockParser,
    inline: InlineParser,
    plugins: List[MarkdownPlugin],
)
```

A synchronous filter for the function used to create `mistune.Markdown` instance to use for parsing markup.

Returns `mistune.Markdown` instance.


## Required arguments

### `action`

```python
def create_markdown_action(
    context: GraphQLContext,
    block: BlockParser,
    inline: InlineParser,
    plugins: List[MarkdownPlugin],
) -> Markdown:
    ...
```

Next filter or built-in function used to create new post in the database.


### `context`

```python
Optional[GraphQLContext]
```

A dict with GraphQL query context.


### `block`

```python
BlockParser
```

An instance of `BlockParser` to use. Defaults to `mistune.BlockParser`.


### `plugins`

```python
List[Callable[[Markdown], None]]
```

List of callables accepting single argument, an instance of `mistune.Markdown`.