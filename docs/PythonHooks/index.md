Python hooks
============

There are three types of hooks in Misago's Python codebase:

- **Actions** that allow injecting additional logic at different parts of the software.
- **Filters** that allow extending built-in functions with custom logic or overriding them altogether.
- **Simple** lists and dicts of additional items that should be added to existing list of items.

Depending on the hook, custom functions should return nothing or value of specified type.

To add custom code to the hook, plugin should import the hook instance from `misago.hooks` and use it's `append` and `prepend` methods as decorators for custom function:

```python
# inside myplugin/plugin.py file
from misago.hooks import graphql_context_hook


@graphql_context_hook.append
async def inject_extra_data_to_graphql_context(get_graphql_context, request):
    # unless your filter replaces built-in logic, it should call the callable passed as first argument.
    # if more plugins are filtering this hook, `get_graphql_context` may be next filter instead!
    context = await get_graphql_context(request)

    # add custom data to context
    context["extra_data"] = "I am plugin!"

    # return context
    return context
```

> All functions injected into hooks must be asynchronous.


Standard hooks
--------------

All standard hooks can be imported from `misago.hooks` module:

- [`authenticate_user_hook`](./authenticate-user-hook.md)
- [`close_thread_hook`](./close-thread-hook.md)
- [`close_thread_input_hook`](./close-thread-input-hook.md)
- [`close_thread_input_model_hook`](./close-thread-input-model-hook.md)
- [`close_threads_hook`](./close-threads-hook.md)
- [`close_threads_input_hook`](./close-threads-input-hook.md)
- [`close_threads_input_model_hook`](./close-threads-input-model-hook.md)
- [`create_post_hook`](./create-post-hook.md)
- [`create_thread_hook`](./create-thread-hook.md)
- [`create_user_hook`](./create-user-hook.md)
- [`create_user_token_hook`](./create-user-token-hook.md)
- [`create_user_token_payload_hook`](./create-user-token-payload-hook.md)
- [`delete_thread_hook`](./delete-thread-hook.md)
- [`delete_thread_input_hook`](./delete-thread-input-hook.md)
- [`delete_thread_input_model_hook`](./delete-thread-input-model-hook.md)
- [`delete_thread_reply_hook`](./delete-thread-reply-hook.md)
- [`delete_thread_reply_input_model_hook`](./delete-thread-reply-input-model-hook.md)
- [`delete_thread_reply_input_reply_hook`](./delete-thread-reply-input-reply-hook.md)
- [`delete_thread_reply_input_thread_hook`](./delete-thread-reply-input-thread-hook.md)
- [`delete_threads_hook`](./delete-threads-hook.md)
- [`delete_threads_input_hook`](./delete-threads-input-hook.md)
- [`delete_threads_input_model_hook`](./delete-threads-input-model-hook.md)
- [`edit_post_hook`](./edit-post-hook.md)
- [`edit_post_input_hook`](./edit-post-input-hook.md)
- [`edit_post_input_model_hook`](./edit-post-input-model-hook.md)
- [`edit_thread_title_hook`](./edit-thread-title-hook.md)
- [`edit_thread_title_input_hook`](./edit-thread-title-input-hook.md)
- [`edit_thread_title_input_model_hook`](./edit-thread-title-input-model-hook.md)
- [`get_auth_user_hook`](./get-auth-user-hook.md)
- [`get_user_from_context_hook`](./get-user-from-context-hook.md)
- [`get_user_from_token_hook`](./get-user-from-token-hook.md)
- [`get_user_from_token_payload_hook`](./get-user-from-token-payload-hook.md)
- [`graphql_context_hook`](./graphql-context-hook.md)
- [`graphql_directives_hook`](./graphql-directives-hook.md)
- [`graphql_type_defs_hook`](./graphql-type-defs-hook.md)
- [`graphql_types_hook`](./graphql-types-hook.md)
- [`jinja2_extensions_hook`](./jinja2-extensions-hook.md)
- [`jinja2_filters_hook`](./jinja2-filters-hook.md)
- [`move_thread_hook`](./move-thread-hook.md)
- [`move_thread_input_hook`](./move-thread-input-hook.md)
- [`move_thread_input_model_hook`](./move-thread-input-model-hook.md)
- [`move_threads_hook`](./move-threads-hook.md)
- [`move_threads_input_hook`](./move-threads-input-hook.md)
- [`move_threads_input_model_hook`](./move-threads-input-model-hook.md)
- [`post_reply_hook`](./post-reply-hook.md)
- [`post_reply_input_hook`](./post-reply-input-hook.md)
- [`post_reply_input_model_hook`](./post-reply-input-model-hook.md)
- [`post_thread_hook`](./post-thread-hook.md)
- [`post_thread_input_hook`](./post-thread-input-hook.md)
- [`post_thread_input_model_hook`](./post-thread-input-model-hook.md)
- [`register_user_hook`](./register-user-hook.md)
- [`register_user_input_hook`](./register-user-input-hook.md)
- [`register_user_input_model_hook`](./register-user-input-model-hook.md)
- [`template_context_hook`](./template-context-hook.md)


Implementing custom action hook
-------------------------------

Action hooks should extend `misago.hooks.ActionHook` generic class, and define custom `call_action` method calling `gather` method defined by `ActionHook`:

```python
from typing import Any, Callable, Coroutine, Dict
from misago.hooks import ActionHook


Action = Callable[[Any], Coroutine[Any, Any, ...]]


class MyActionHook(ActionHook[Action]):
    async def call_action(self, arg: Any) -> Any:
        return await self.gather(arg)


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