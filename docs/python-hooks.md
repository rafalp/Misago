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

All standard hooks are defined in `misago.hooks` package and can be imported from it:


### `create_user_hook`:

```python
create_user_hook.call_action(
    action: CreateUserAction,
    name: str,
    email: str,
    *,
    password: Optional[str] = None,
    is_moderator: bool = False,
    is_admin: bool = False,
    joined_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None
)
```

A filter for the function used to create new user account in the database.

Returns `User` dict with newly created user data.


#### Required arguments

##### `action`

```python
async def create_user(
    name: str,
    email: str,
    *,
    password: Optional[str] = None,
    is_moderator: bool = False,
    is_admin: bool = False,
    joined_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None
) -> User:
    ...
```

Next filter or built-in function used to create new user account in the database.


##### `name`

```python
str
```

User name.


##### `email`

```python
str
```

User e-mail address.


#### Optional arguments

##### `password`

```python
Optional[str] = None
```

User password. If not set, user will not be able to log-in to their account using default method.


##### `is_moderator`

```python
bool = False
```

Controls if user can moderate site.


##### `is_admin`

```python
bool = False
```

Controls if user user can administrate the site.


##### `joined_at`

```python
Optional[datetime] = datetime.now()
```

Joined at date for this user-account. Defaults to current date-time.


##### `extra`

```python
Optional[Dict[str, Any]] = dict()
```

JSON-serializable dict with extra data for this user. This value is not used by Misago, but allows plugin authors to store additional information about user directly on their database row.


- - -


### `create_user_token_hook`

```python
create_user_token_hook.call_action(action: CreateUserTokenAction, context: GraphQLContext, user: User)
```

A filter for the function used to create an authorization token for user.

Returns `str` with authorization token that should be included by the client in `Authorization` header in future calls to the API.


#### Required arguments

##### `action`

```python
async def create_user_token(context: GraphQLContext, user: User) -> str:
    ...
```

Next filter or built-in function used to create authorization token for user.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


#### `user`

```python
User
```

A `dict` containing authorized user's data.


- - -


### `create_user_token_payload_hook`

```python
create_user_token_payload_hook.call_action(action: CreateUserTokenPayloadAction, context: GraphQLContext, user: User)
```

A filter for the function used to create an payload for user authorization token.

Returns `dict` which should be used as JWT token's payload.


#### Required arguments

##### `action`

```python
async def create_user_token_payload(context: GraphQLContext, user: User) -> Dict[str, Any]:
    ...
```

Next filter or built-in function used to create payload for user authorization token.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


#### `user`

```python
User
```

A `dict` containing authorized user's data.


- - -


### `graphql_context_hook`

```python
graphql_context_hook.call_action(action: GraphQLContextAction, request: Request)
```

A filter for the function used to create a GraphQL context.

Returns `GraphQLContext` dict with current GraphQL query context.


#### Required arguments

##### `action`

```python
async def get_graphql_context(request: Request) -> GraphQLContext:
    ...
```

Next filter or built-in function used to create GraphQL context.


#### `request`

```python
Request
```

An instance of [`Request`](https://www.starlette.io/requests/) representing current HTTP request to GraphQL API.


- - -


### `graphql_directives_hook`

`dict` of [`SchemaDirectiveVisitor`](https://ariadnegraphql.org/docs/api-reference#schemadirectivevisitor) sub-types that should be added to GraphQL API.

See Ariadne [Schema Directives](https://ariadnegraphql.org/docs/schema-directives) documentation for examples.

> **Note:** Plugin adding directive to the GraphQL API should also use the `graphql_type_defs_hook` to add custom directive definition to GraphQL schema.


#### Example

```python
from ariadne import SchemaDirectiveVisitor
from misago.hooks import graphql_directives_hook


class MyDirective(SchemaDirectiveVisitor):
    ...


graphql_directives_hook["myDirective"] = MyDirective
```


- - -


### `graphql_type_defs_hook`

`list` of `str` containing GraphQL type definitions in GraphQL Schema Definition Language that should be added to the GraphQL schema.


#### Example

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


### `graphql_types_hook`

`list` of [Ariadne bindables](https://ariadnegraphql.org/docs/resolvers) that should be added to GraphQL API.


#### Example

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


### `register_input_hook`

```python
register_input_hook.call_action(
    action: RegisterInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[Union[AsyncRootValidator, AsyncValidator]]],
    data: RegisterInput,
    errors_list: ErrorsList
)
```

A filter for the function used to validate data for `RegisterInput` GraphQL input type.

Returns a tuple of `data` that should be used to create new user and validation `errors`.


#### Required arguments

##### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Union[AsyncRootValidator, AsyncValidator]]],
    cleaned_data: RegisterInput,
    errors: ErrorsList,
) -> Tuple[RegisterInput, ErrorsList]:
    ...
```

Next filter or built-in function used to validate registration input data.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `validators`

```python
Dict[str, List[Union[AsyncValidator, AsyncRootValidator]]]
```

A dict of lists of validators that should be used to validate inputs values.


##### `data`

```python
Dict[str, Any]
```

A dict with input data that passed initial cleaning and validation. If any of fields failed initial cleanup and validation, it won't be present in this dict.


##### `errors`

```python
ErrorsList
```

List of validation errors found so far. Can be extended using it's `add_error` and `add_root_error` methods.


- - -


### `register_input_model_hook`

```python
register_input_model_hook.call_action(action: RegisterInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `RegisterInput` GraphQL input type.

Returns `RegisterInputModel` input model type.


#### Required arguments

##### `action`

```python
async def create_input_model(context: GraphQLContext) -> RegisterInputModel:
    ...
```

Next filter or built-in function used to create input model type.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


### `register_user_hook`

```python
register_user_hook.call_action(
    action: RegisterUserAction,
    context: GraphQLContext,
    cleaned_data: RegisterInput
)
```

A filter for the function used by GraphQL mutation registering new user account to register new user in the database.

Returns `User` dict with newly created user data.


#### Required arguments

##### `action`

```python
async def register_user(context: GraphQLContext, cleaned_data: RegisterInput) -> User:
    ...
```

Next filter or built-in function used to register new user account in the database.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `name`, `email` and `password` keys, all being strings.


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