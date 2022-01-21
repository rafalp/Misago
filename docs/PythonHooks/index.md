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


### `misago.auth.hooks`

- [`authenticate_user_hook`](./authenticate-user-hook.md)
- [`create_user_token_hook`](./create-user-token-hook.md)
- [`create_user_token_payload_hook`](./create-user-token-payload-hook.md)
- [`get_auth_user_hook`](./get-auth-user-hook.md)
- [`get_user_from_context_hook`](./get-user-from-context-hook.md)
- [`get_user_from_token_hook`](./get-user-from-token-hook.md)
- [`get_user_from_token_payload_hook`](./get-user-from-token-payload-hook.md)


### `misago.categories.hooks`

- [`delete_categories_contents_hook`](./delete-categories-contents-hook.md)
- [`move_categories_contents_hook`](./move-categories-contents-hook.md)


### `misago.graphql.hooks`

- [`graphql_admin_directives_hook`](./graphql-admin-directives-hook.md)
- [`graphql_admin_type_defs_hook`](./graphql-admin-type-defs-hook.md)
- [`graphql_admin_types_hook`](./graphql-admin-types-hook.md)
- [`graphql_context_hook`](./graphql-context-hook.md)
- [`graphql_directives_hook`](./graphql-directives-hook.md)
- [`graphql_type_defs_hook`](./graphql-type-defs-hook.md)
- [`graphql_types_hook`](./graphql-types-hook.md)


### `misago.graphql.public.mutations.hooks.postcreate`

- [`post_create_hook`](./post-create-hook.md)
- [`post_create_input_hook`](./post-create-input-hook.md)
- [`post_create_input_model_hook`](./post-create-input-model-hook.md)


### `misago.graphql.public.mutations.hooks.postdelete`

- [`post_delete_hook`](./post-delete-hook.md)
- [`post_delete_input_post_hook`](./post-delete-input-post-hook.md)
- [`post_delete_input_thread_hook`](./post-delete-input-thread-hook.md)


### `misago.graphql.public.mutations.hooks.postsbulkdelete`

- [`posts_bulk_delete_hook`](./posts-bulk-delete-hook.md)
- [`posts_bulk_delete_input_posts_hook`](./posts-bulk-delete-input-posts-hook.md)
- [`posts_bulk_delete_input_thread_hook`](./posts-bulk-delete-input-thread-hook.md)


### `misago.graphql.public.mutations.hooks.postupdate`

- [`post_update_hook`](./post-update-hook.md)
- [`post_update_input_hook`](./post-update-input-hook.md)
- [`post_update_input_model_hook`](./post-update-input-model-hook.md)


### `misago.graphql.public.mutations.hooks.usercreate`

- [`user_create_hook`](./user-create-hook.md)
- [`user_create_input_hook`](./user-create-input-hook.md)
- [`user_create_input_model_hook`](./user-create-input-model-hook.md)


### `misago.graphql.public.mutations.hooks.threadclose`

- [`thread_close_hook`](./thread-close-hook.md)
- [`thread_close_input_hook`](./thread-close-input-hook.md)


### `misago.graphql.public.mutations.hooks.threadcreate`

- [`thread_create_hook`](./thread-create-hook.md)
- [`thread_create_input_hook`](./thread-create-input-hook.md)
- [`thread_create_input_model_hook`](./thread-create-input-model-hook.md)


### `misago.graphql.public.mutations.hooks.threaddelete`

- [`thread_delete_hook`](./thread-delete-hook.md)
- [`thread_delete_input_hook`](./thread-delete-input-hook.md)


### `misago.graphql.public.mutations.hooks.threadmove`

- [`thread_move_hook`](./thread-category-update-hook.md)
- [`thread_move_input_hook`](./thread-category-update-input-hook.md)


### `misago.graphql.public.mutations.hooks.threadopen`

- [`thread_open_hook`](./thread-open-hook.md)
- [`thread_open_input_hook`](./thread-open-input-hook.md)


### `misago.graphql.public.mutations.hooks.threadrename`

- [`thread_rename_hook`](./thread-rename-hook.md)
- [`thread_rename_input_hook`](./thread-rename-input-hook.md)


### `misago.graphql.public.mutations.hooks.threadsbulkclose`

- [`threads_bulk_close_hook`](./threads-bulk-close-hook.md)
- [`threads_bulk_close_input_hook`](./threads-bulk-close-input-hook.md)


### `misago.graphql.public.mutations.hooks.threadsbulkdelete`

- [`threads_bulk_delete_hook`](./threads-bulk-delete-hook.md)
- [`threads_bulk_delete_input_hook`](./threads-bulk-delete-input-hook.md)


### `misago.graphql.public.mutations.hooks.threadsbulkmove`

- [`threads_bulk_move_hook`](./threads-bulk-move-hook.md)
- [`threads_bulk_move_input_hook`](./threads-bulk-move-input-hook.md)


### `misago.graphql.public.mutations.hooks.threadsbulkopen`

- [`threads_bulk_open_hook`](./threads-bulk-open-hook.md)
- [`threads_bulk_open_input_hook`](./threads-bulk-open-input-hook.md)


### `misago.richtext.hooks`

- [`convert_block_ast_to_rich_text_hook`](./convert-block-ast-to-rich-text-hook.md)
- [`convert_inline_ast_to_text_hook`](./convert-inline-ast-to-text-hook.md)
- [`convert_rich_text_block_to_html_hook`](./convert-rich-text-block-to-html-hook.md)
- [`convert_rich_text_to_html_hook`](./convert-rich-text-to-html-hook.
- [`create_markdown_hook`](./create-markdown-hook.md)
- [`markdown_hook`](./markdown-hook.md)
- [`parse_markup_hook`](./parse-markup-hook.md)
- [`update_markup_metadata_hook`](./update-markup-metadata-hook.md)


### `misago.routes.hooks`

- [`exception_handlers_hook`](./exception-handlers-hook.md)
- [`register_routes_hook`](./register-routes-hook.md)


### `misago.template.hooks`

- [`jinja2_extensions_hook`](./jinja2-extensions-hook.md)
- [`jinja2_filters_hook`](./jinja2-filters-hook.md)
- [`template_context_hook`](./template-context-hook.md)


### `misago.threads.hooks`

- [`create_post_hook`](./create-post-hook.md)
- [`create_thread_hook`](./create-thread-hook.md)
- [`update_post_hook`](./update-post-hook.md)


### `misago.users.hooks`

- [`create_user_hook`](./create-user-hook.md)


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
    def call_action(self, action: Action, arg: Any) -> Any:
        return self.filter(action, request, context)


my_hook = MyFilterHook()
```


### Making filters synchronous

If filter hook is not intended to perform any IO, you can declare it as synchronous by defining `is_async = False` on it:


```python
class MyFilterHook(FilterHook[Action, Filter]):
    is_async = False

    def call_action(self, action: Action, arg: Any) -> Any:
        return self.filter(action, request, context)
```

This hook will no longer return awaitable from `self.filter`.