Python hooks
============

There are two types of hooks in Misago's Python codebase:

- **Actions** that allow injecting additional logic at different parts of the software.
- **Filters** that allow extending built-in functions with custom logic or overriding them altogether.

Depending on the hook, custom functions should return nothing or value of specified type.

To add custom code to the hook, plugin should import the hook instance from `misago.hooks` and use it's `append` and `prepend` methods as decorators for custom function:

```python
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

A filter for the function used to create a GraphQL context. Is called with three arguments:

- `get_graphql_context: Callable[[request, context], Coroutine[context]]` - next filter in hook or original function implemented by Misago.
- `request: Request` - an instance of [`Request`](https://www.starlette.io/requests/) representing current HTTP request to GraphQL API.
- `context: Dict[str, Any]` - a dict with context that will be made available to GraphQL resolvers executing this request's query.

Filter should return `Dict[str, Any]` with a context.


### `register_input_hook`

A filter for the function used to validate data for `RegisterInput` GraphQL input type. Is called with five arguments:

- `create_input_model: RegisterInputAction` - next filter in hook or original function implemented by Misago.
- `context: GraphQLContext` - a dict with context that will be made available to GraphQL resolvers executing this request's query.
- `validators: Dict[str, List[Union[AsyncValidator, AsyncRootValidator]]]` - a dict of async data validators that should be used in data validation.
- `data: Dict[str, Any]` - dict with cleaned data that should be validated and used to create new user. This dict will contain only valid keys.
- `errors: ErrorsList` - list of validation errors.

Filter should return a tuple of `data` that should be used to create new user and validation `errors`.


### `register_input_model_hook`

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `RegisterInput` GraphQL input type. Is called with two arguments:

- `create_input_model: Callable[[GraphQLContext], Coroutine[Model]]` - next filter in hook or original function implemented by Misago.
- `context: GraphQLContext` - a dict with context that will be made available to GraphQL resolvers executing this request's query.

Filter should return new Pydantic model to use for validating input data.


Implementing custom action hook
-------------------------------

Action hooks should extend `misago.hooks.ActionHook` generic class, and define custom `call_action` method:

```python
from typing import Any, Callable, Coroutine, Dict
from misago.hooks import ActionHook


Action = Callable[[Any], Coroutine[Any, Any, ...]]


class MyActionHook(ActionHook[Action]):
    async def call_action(self, arg: Any) -> Any:
        return await super().call_action(arg)


my_hook = MyActionHook()
```


Implementing custom filter hook
-------------------------------

Filters hooks should extend `misago.hooks.FilterHook` generic class, and define custom `call_action` method that uses `filter` method provided by base class:

```python
from typing import Any, Callable, Coroutine, Dict
from misago.hooks import FilterHook


Action = Callable[[Any], Coroutine[Any, Any, ...]]
Filter = Callable[[Action, Any], Coroutine[Any, Any, ...]]


class MyFilterHook(FilterHook[Action, Filter]):
    async def call_action(self, action: Action, arg: Any) -> Any:
        return await self.filter(action, request, context)


my_hook = MyFilterHook()
```