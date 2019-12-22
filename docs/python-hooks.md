# `graphql_context_hook`

```python
graphql_context_hook.call_action(action: GraphQLContextAction, request: Request)
```

A filter for the function used to create a GraphQL context.

Returns `GraphQLContext` dict with current GraphQL query context.


## Required arguments

### `action`

```python
async def get_graphql_context(request: Request) -> GraphQLContext:
    ...
```

Next filter or built-in function used to create GraphQL context.


## `request`

```python
Request
```

An instance of [`Request`](https://www.starlette.io/requests/) representing current HTTP request to GraphQL API.


- - -


# `graphql_directives_hook`

`dict` of [`SchemaDirectiveVisitor`](https://ariadnegraphql.org/docs/api-reference#schemadirectivevisitor) sub-types that should be added to GraphQL API.

See Ariadne [Schema Directives](https://ariadnegraphql.org/docs/schema-directives) documentation for examples.

> **Note:** Plugin adding directive to the GraphQL API should also use the `graphql_type_defs_hook` to add custom directive definition to GraphQL schema.


## Example

```python
from ariadne import SchemaDirectiveVisitor
from misago.hooks import graphql_directives_hook


class MyDirective(SchemaDirectiveVisitor):
    ...


graphql_directives_hook["myDirective"] = MyDirective
```


- - -


# `graphql_type_defs_hook`

`list` of `str` containing GraphQL type definitions in GraphQL Schema Definition Language that should be added to the GraphQL schema.


## Example

Add new type `Like` to GraphQL schema:

```python
from ariadne import gql
from misago.hooks import graphql_type_defs_hook


graphql_type_defs_hook.append(
    gql(
        """
            type Like {
                id: ID
                created_at: DateTime
                post: Post
            }

            extend type Post {
                likes: [Like]
            }
        """
    )
)
```


- - -


# `graphql_types_hook`

A `list` of [Ariadne bindables](https://ariadnegraphql.org/docs/resolvers) that should be added to GraphQL API.


## Example

```python
from ariadne import TypeObject
from misago.hooks import graphql_types_hook
from misago.loaders import load_post


like_type = TypeObject("Like)


@like_type.field("post"):
async def resolve_like_post(obj, _):
    return await load_post(obj["post_id"])


graphql_types_hook.append(like_type)
```


- - -


# `jinja2_extensions`

A `list` of [Jinja extensions](https://jinja.palletsprojects.com/en/2.10.x/extensions/#jinja-extensions) that should be used by template engine.


- - -


# `jinja2_filters`

A `dict` of [Jinja filters](https://jinja.palletsprojects.com/en/2.10.x/api/#custom-filters) that should be used by template engine.


- - -


# `post_reply_hook`

```python
post_reply_hook.call_action(
    action: PostReplyAction,
    context: GraphQLContext,
    cleaned_data: PostReplyInput,
)
```

A filter for the function used by GraphQL mutation creating new reply to create new reply in the database.

Returns tuple of `Thread` and `Post` dataclasses with newly created reply data.


## Required arguments

### `action`

```python
async def post_reply(
    context: GraphQLContext,
    cleaned_data: PostReplyInput,
) -> Tuple[Thread, Post]:
    ...
```

Next filter or built-in function used to create new reply in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `thread` and `body` keys:

```python
class PostReplyInput(TypedDict):
    thread: Thread
    body: str
```


- - -


# `post_reply_input_hook`

```python
post_reply_hook.call_action(
    action: PostReplyInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: PostReplyInput,
    errors_list: ErrorsList,
)
```

A filter for the function used to validate data for `PostReplyInputModel` GraphQL input type.

Returns a tuple of `data` that should be used to create new reply and validation `errors`.


## Required arguments

### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: PostReplyInput,
    errors: ErrorsList,
) -> Tuple[PostReplyInput, ErrorsList]:
    ...
```

Next filter or built-in function used to validate new reply input data.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `validators`

```python
Dict[str, List[AsyncValidator]]
```

A dict of lists of validators that should be used to validate inputs values.


### `data`

```python
Dict[str, Any]
```

A dict with input data that passed initial cleaning and validation. If any of fields failed initial cleanup and validation, it won't be present in this dict.


### `errors`

```python
ErrorsList
```

List of validation errors found so far. Can be extended using it's `add_error` and `add_root_error` methods.


- - -


# `post_reply_input_model_hook`

```python
post_reply_input_model_hook.call_action(action: PostReplyInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `PostReplyInputModel` GraphQL input type used by the "post reply" GraphQL mutation.

Returns `PostReplyInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> PostReplyInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


# `post_thread_hook`

```python
post_thread_hook.call_action(
    action: PostThreadAction,
    context: GraphQLContext,
    cleaned_data: PostThreadInput,
)
```

A filter for the function used by GraphQL mutation creating new thread to create new thread in the database.

Returns tuple of `Thread` and `Post` dataclasses with newly created thread data.


## Required arguments

### `action`

```python
async def post_thread(
    context: GraphQLContext,
    cleaned_data: PostThreadInput,
) -> Tuple[Thread, Post]:
    ...
```

Next filter or built-in function used to create new thread in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `category`, `title` and `body` keys:

```python
class PostThreadInput(TypedDict):
    category: Category
    title: str
    body: str
```


- - -


# `post_thread_input_hook`

```python
post_thread_hook.call_action(
    action: PostThreadInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: PostThreadInput,
    errors_list: ErrorsList,
)
```

A filter for the function used to validate data for `PostThreadInputModel` GraphQL input type.

Returns a tuple of `data` that should be used to create new thread and validation `errors`.


## Required arguments

### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: PostThreadInput,
    errors: ErrorsList,
) -> Tuple[PostThreadInput, ErrorsList]:
    ...
```

Next filter or built-in function used to validate new thread input data.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `validators`

```python
Dict[str, List[AsyncValidator]]
```

A dict of lists of validators that should be used to validate inputs values.


### `data`

```python
Dict[str, Any]
```

A dict with input data that passed initial cleaning and validation. If any of fields failed initial cleanup and validation, it won't be present in this dict.


### `errors`

```python
ErrorsList
```

List of validation errors found so far. Can be extended using it's `add_error` and `add_root_error` methods.


- - -


# `post_thread_input_model_hook`

```python
post_thread_input_model_hook.call_action(action: PostThreadInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `PostThreadInputModel` GraphQL input type used by the "post thread" GraphQL mutation.

Returns `PostThreadInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> PostThreadInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


# `register_user_input_hook`

```python
register_user_input_hook.call_action(
    action: RegisterUserInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: RegisterUserInput,
    errors_list: ErrorsList
)
```

A filter for the function used to validate data for `RegisterUserInputModel` GraphQL input type.

Returns a tuple of `data` that should be used to create new user and validation `errors`.


## Required arguments

### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: RegisterUserInput,
    errors: ErrorsList,
) -> Tuple[RegisterUserInput, ErrorsList]:
    ...
```

Next filter or built-in function used to validate registration input data.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `validators`

```python
Dict[str, List[AsyncValidator]]
```

A dict of lists of validators that should be used to validate inputs values.


### `data`

```python
Dict[str, Any]
```

A dict with input data that passed initial cleaning and validation. If any of fields failed initial cleanup and validation, it won't be present in this dict.


### `errors`

```python
ErrorsList
```

List of validation errors found so far. Can be extended using it's `add_error` and `add_root_error` methods.


- - -


# `register_user_input_model_hook`

```python
register_user_input_model_hook.call_action(action: RegisterUserInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `RegisterUserInputModel` GraphQL input type used by the "register new user" GraphQL mutation.

Returns `RegisterUserInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> RegisterUserInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


# `register_user_hook`

```python
register_user_hook.call_action(
    action: RegisterUserAction,
    context: GraphQLContext,
    cleaned_data: RegisterUserInput
)
```

A filter for the function used by GraphQL mutation registering new user account to register new user in the database.

Returns `User` dataclass with newly created user data.


## Required arguments

### `action`

```python
async def register_user(context: GraphQLContext, cleaned_data: RegisterUserInput) -> User:
    ...
```

Next filter or built-in function used to register new user account in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `name`, `email` and `password` keys, all being strings.


- - -


# `template_context_hook`

```python
template_context_hook.call_action(action: TemplateContextAction, request: Request)
```

A filter for the function used to create default template context.

Returns `TemplateContext` dict with default template context.


## Required arguments

### `action`

```python
async def get_default_context(request: Request) -> TemplateContext:
    ...
```

Next filter or built-in function used to create a template context.


## `request`

```python
Request
```

An instance of [`Request`](https://www.starlette.io/requests/) representing current HTTP request to application.
