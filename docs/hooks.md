Hooks
=====

There are two types of hooks in Misago's Python codebase:

- **Filters** that allow extending built-in functions with custom logic or overriding them altogether.
- **Actions** that allow injecting additional logic at different parts of the software.

To add custom code to hook, plugin should import hook instance from `misago.hooks` and use it's `append` and `prepend` methods as decorators for custom function:

```
# inside myplugin/plugin.py file
from misago.hooks import graphql_context_hook


@graphql_context_hook.append
async def inject_extra_data_to_graphql_context(get_graphql_context, request, context):
    # call Misago function to obtain default GraphQL context values
    # if more plugins are filtering this hook, `get_graphql_context` may be next filter instead!
    context = await get_graphql_context(request, context)

    # add custom data to context
    context["extra_data"] = "I am plugin!"

    # return context
    return context

```

> All functions injected into hooks must be asynchronous.


Standard hooks
--------------

All standard hooks are defined in `misago.hooks` package and can be imported from it:


### `graphql_context_hook`

A filter for function Misago calls to retrieve GraphQL context. Is called with three arguments:

- `get_graphql_context: Callable[[request, context], Coroutine[context]]` - next filter in hook or original function implemented by Misago.
- `request: Request` - an instance of [`Request`](https://www.starlette.io/requests/) representing current HTTP request to GraphQL API.
- `context: Dict[str, Any]` - a dict with context that will be made available to GraphQL resolvers executing this request's query.

Filter should return `Dict[str, Any]` with a context.


Implementing custom hooks
-------------------------
