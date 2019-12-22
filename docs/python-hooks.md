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


### `authenticate_user_hook`

```python
authenticate_user_hook.call_action(
    action: AuthenticateUserAction,
    context: GraphQLContext,
    username: str,
    password: str,
)
```

A filter for the function used to authenticate user for given user name/email and password.

Returns `User` dataclass with authenticated user data or `None` if user should not be able to authenticate (eg. deactivated or invalid credentials).


#### Required arguments

##### `action`

```python
async def authenticate_user(
    context: GraphQLContext,
    username: str,
    password: str,
) -> Optional[User:]
    ...
```

Next filter or built-in function used to authenticate user for given credentials.


##### `username`

```python
str
```

User name or e-mail address.


##### `password`

```python
str
```

User password.


- - -


### `close_thread_hook`

```python
close_thread_hook.call_action(
    action: CloseThreadAction,
    context: GraphQLContext,
    cleaned_data: CloseThreadInput,
)
```

A filter for the function used by GraphQL mutation closing to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


#### Required arguments

##### `action`

```python
async def close_thread(context: GraphQLContext, cleaned_data: CloseThreadInput) -> Thread:
    ...
```

Next filter or built-in function used to update the thread in the database.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `thread` and `is_closed` keys:

```python
class CloseThreadInput(TypedDict):
    thread: Thread
    is_closed: bool
```


- - -


### `close_thread_input_hook`

```python
close_thread_hook.call_action(
    action: CloseThreadInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: CloseThreadInput,
    errors_list: ErrorsList,
)
```

A filter for the function used to validate data for `CloseThreadInputModel` GraphQL input type.

Returns a tuple of `data` that should be used to update the thread and validation `errors`.


#### Required arguments

##### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: CloseThreadInput,
    errors: ErrorsList,
) -> Tuple[CloseThreadInput, ErrorsList]:
    ...
```

Next filter or built-in function used to validate closed thread input data.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `validators`

```python
Dict[str, List[AsyncValidator]]
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


### `close_thread_input_model_hook`

```python
close_thread_input_model_hook.call_action(action: CloseThreadInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `CloseThreadInputModel` GraphQL input type used by the "thread reply" GraphQL mutation.

Returns `CloseThreadInputModel` input model type.


#### Required arguments

##### `action`

```python
async def create_input_model(context: GraphQLContext) -> CloseThreadInputModel:
    ...
```

Next filter or built-in function used to create input model type.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


### `create_post_hook`:

```python
create_post_hook.call_action(
    action: CreatePostAction,
    thread: Thread,
    body: dict,
    *,
    poster: Optional[User] = None,
    poster_name: Optional[str] = None,
    edits: Optional[int] = 0,
    posted_at: Optional[datetime] = None,
    extra: Optional[dict] = None,
)
```

A filter for the function used to create new post in the database.

Returns `Post` dataclass with newly created post data.


#### Required arguments

##### `action`

```python
async def create_post(
    thread: Thread,
    body: dict,
    *,
    poster: Optional[User] = None,
    poster_name: Optional[str] = None,
    edits: Optional[int] = 0,
    posted_at: Optional[datetime] = None,
    extra: Optional[dict] = None,
) -> Thread:
    ...
```

Next filter or built-in function used to create new post in the database.


##### `thread`

```python
Thread
```

`Thread` dataclass for thread in which thread will be created.


##### `body`

```python
dict
```

`dict` containing JSON with [ProseMirror](https://prosemirror.net) document representing post body.


#### Optional arguments

##### `poster`

```python
Optional[User] = None
```

`User` dataclass with post creator.


##### `starter_name`

```python
Optional[str] = None
```

`str` with post creator name. Is mutually exclusive with `poster` argument. If given instead of `poster`, this means post creator was guest user.


##### `edits`

```python
int = False
```

Initial count of number of times that post has been edited.


##### `posted_at`

```python
Optional[datetime] = datetime.utcnow()
```

`datetime` of post creation.


##### `extra`

```python
Optional[Dict[str, Any]] = dict()
```

JSON-serializable dict with extra data for this post. This value is not used by Misago, but allows plugin authors to store additional information about post directly on it's database row.


- - -


### `create_thread_hook`:

```python
create_thread_hook.call_action(
    action: CreateThreadAction,
    category: Category,
    title: str,
    *,
    first_post: Optional[Post] = None,
    starter: Optional[User] = None,
    starter_name: Optional[str] = None,
    replies: int = 0,
    is_closed: bool = False,
    started_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None,
)
```

A filter for the function used to create new thread in the database.

Returns `Thread` dataclass with newly created thread data.

> **Note:** Misago requires for thread to exist in the database before thread first post can be created. Most of times this method will be called with `first_post` being empty and updated later.


#### Required arguments

##### `action`

```python
async def create_thread(
    category: Category,
    title: str,
    *,
    first_post: Optional[Post] = None,
    starter: Optional[User] = None,
    starter_name: Optional[str] = None,
    replies: int = 0,
    is_closed: bool = False,
    started_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Thread:
    ...
```

Next filter or built-in function used to create new thread in the database.


##### `category`

```python
Category
```

`Category` dataclass for category in which thread will be created.


##### `title`

```python
str
```

String with thread title.


#### Optional arguments

##### `first_post`

```python
Optional[Post] = None
```

`Post` dataclass with thread first post.


##### `starter`

```python
Optional[User] = None
```

`User` dataclass with thread starter.


##### `starter_name`

```python
Optional[str] = None
```

`str` with thread starter name. Is mutually exclusive with `starter` argument. If given instead of `starter`, this means thread creator was guest user.


##### `replies`

```python
int = False
```

Initial count of thread replies.


#####  `is_closed`

```python
bool = False
```

Controls if thread should be created closed.


##### `started_at`

```python
Optional[datetime]
```

`datetime` of thread creation. Mutually exclusive with `first_post`. If `first_post` is given, it's `posted_at` `datetime` will be used instead.


##### `extra`

```python
Optional[Dict[str, Any]] = dict()
```

JSON-serializable dict with extra data for this thread. This value is not used by Misago, but allows plugin authors to store additional information about thread directly on it's database row.


- - -


### `create_user_hook`:

```python
create_user_hook.call_action(
    action: CreateUserAction,
    name: str,
    email: str,
    *,
    password: Optional[str] = None,
    is_deactivated: bool = False,
    is_moderator: bool = False,
    is_admin: bool = False,
    joined_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None
)
```

A filter for the function used to create new user account in the database.

Returns `User` dataclass with newly created user data.


#### Required arguments

##### `action`

```python
async def create_user(
    name: str,
    email: str,
    *,
    password: Optional[str] = None,
    is_deactivated: bool = False,
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
Optional[datetime] = datetime.utcnow()
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


### `edit_post_hook`

```python
edit_post_hook.call_action(
    action: EditPostAction,
    context: GraphQLContext,
    cleaned_data: EditPostInput,
)
```

A filter for the function used by GraphQL mutation editing post to update the post in the database.

Returns `Post` dataclass with updated post data.


#### Required arguments

##### `action`

```python
async def edit_post(context: GraphQLContext, cleaned_data: EditPostInput) -> Post:
    ...
```

Next filter or built-in function used to update the post in the database.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `post` and `body` keys:

```python
class EditPostInput(TypedDict):
    post: Post
    body: str
```


- - -


### `edit_post_input_hook`

```python
edit_post_hook.call_action(
    action: EditPostInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: EditPostInput,
    errors_list: ErrorsList,
)
```

A filter for the function used to validate data for `EditPostInputModel` GraphQL input type.

Returns a tuple of `data` that should be used to update the post and validation `errors`.


#### Required arguments

##### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: EditPostInput,
    errors: ErrorsList,
) -> Tuple[EditPostInput, ErrorsList]:
    ...
```

Next filter or built-in function used to validate edited post input data.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `validators`

```python
Dict[str, List[AsyncValidator]]
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


### `edit_post_input_model_hook`

```python
edit_post_input_model_hook.call_action(action: EditPostInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `EditPostInputModel` GraphQL input type used by the "post reply" GraphQL mutation.

Returns `EditPostInputModel` input model type.


#### Required arguments

##### `action`

```python
async def create_input_model(context: GraphQLContext) -> EditPostInputModel:
    ...
```

Next filter or built-in function used to create input model type.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


### `edit_thread_title_hook`

```python
edit_thread_title_hook.call_action(
    action: EditThreadTitleAction,
    context: GraphQLContext,
    cleaned_data: EditThreadTitleInput,
)
```

A filter for the function used by GraphQL mutation editing thread title to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


#### Required arguments

##### `action`

```python
async def edit_thread_title(context: GraphQLContext, cleaned_data: EditThreadTitleInput) -> Thread:
    ...
```

Next filter or built-in function used to update the thread in the database.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `thread` and `title` keys:

```python
class EditThreadTitleInput(TypedDict):
    thread: Thread
    title: str
```


- - -


### `edit_thread_title_input_hook`

```python
edit_thread_title_hook.call_action(
    action: EditThreadTitleInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: EditThreadTitleInput,
    errors_list: ErrorsList,
)
```

A filter for the function used to validate data for `EditThreadTitleInputModel` GraphQL input type.

Returns a tuple of `data` that should be used to update the thread and validation `errors`.


#### Required arguments

##### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: EditThreadTitleInput,
    errors: ErrorsList,
) -> Tuple[EditThreadTitleInput, ErrorsList]:
    ...
```

Next filter or built-in function used to validate edited thread input data.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `validators`

```python
Dict[str, List[AsyncValidator]]
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


### `edit_thread_title_input_model_hook`

```python
edit_thread_title_input_model_hook.call_action(action: EditThreadTitleInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `EditThreadTitleInputModel` GraphQL input type used by the "thread reply" GraphQL mutation.

Returns `EditThreadTitleInputModel` input model type.


#### Required arguments

##### `action`

```python
async def create_input_model(context: GraphQLContext) -> EditThreadTitleInputModel:
    ...
```

Next filter or built-in function used to create input model type.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


### `get_auth_user_hook`

```python
get_auth_user_hook.call_action(action: GetAuthUserAction, context: GraphQLContext, user_id: int)
```

A filter for the function used to get authorized user for given auth credential (eg. token).

Returns `User` dataclass with authorized user data or `None` if user was not found or couldn't be authenticated for other reason (eg. deactivated).


#### Required arguments

##### `action`

```python
async def get_user(context: GraphQLContext, user_id: int) -> Optional[User]:
    ...
```

Next filter or built-in function used to obtain authorized user by their id.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


#### `user_id`

```python
int
```

An `int` containing authorized user's id. May no longer exist in database.


- - -


### `get_user_from_context_hook`


```python
get_user_from_token_hook.get_user_from_context_hook(action: GetUserFromContextAction, context: GraphQLContext)
```

A filter for the function used to get user for current context.

Returns `User` dataclass with authorized user data or `None` if context didn't contain data required to resolve authorized user.


#### Required arguments

##### `action`

```python
async def get_user_from_context(context: GraphQLContext) -> Optional[User]:
    ...
```

Next filter or built-in function used to obtain user for current context.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


### `get_user_from_token_hook`

```python
get_user_from_token_hook.call_action(action: GetUserFromTokenAction, context: GraphQLContext, token: str)
```

A filter for the function used to get user for given authorization token.

Returns `User` dataclass with authorized user data or `None` if token was invalid or expired.


#### Required arguments

##### `action`

```python
async def get_user_from_token(context: GraphQLContext, token: str) -> Optional[User]:
    ...
```

Next filter or built-in function used to obtain user for authorization token.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


#### `token`

```python
str
```

A `str` containing authorization token. It may be invalid.


- - -


### `get_user_from_token_payload_hook`

```python
get_user_from_token_payload_hook.call_action(action: GetUserFromTokenAction, context: GraphQLContext, payload: Dict[str, Any])
```

A filter for the function used to get user for given authorization token payload.

Returns `User` dataclass with authorized user data or `None` if token's payload was invalid or expired.


#### Required arguments

##### `action`

```python
async def get_user_from_token_payload(context: GraphQLContext, token_payload: Dict[str, any]) -> Optional[User]:
    ...
```

Next filter or built-in function used to obtain user for authorization token payload.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


#### `payload`

```python
Dict[str, Any]
```

A `dict` containing payload extracted from authorization token.


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

A `list` of [Ariadne bindables](https://ariadnegraphql.org/docs/resolvers) that should be added to GraphQL API.


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


### `jinja2_extensions`

A `list` of [Jinja extensions](https://jinja.palletsprojects.com/en/2.10.x/extensions/#jinja-extensions) that should be used by template engine.


- - -


### `jinja2_filters`

A `dict` of [Jinja filters](https://jinja.palletsprojects.com/en/2.10.x/api/#custom-filters) that should be used by template engine.


- - -


### `post_reply_hook`

```python
post_reply_hook.call_action(
    action: PostReplyAction,
    context: GraphQLContext,
    cleaned_data: PostReplyInput,
)
```

A filter for the function used by GraphQL mutation creating new reply to create new reply in the database.

Returns tuple of `Thread` and `Post` dataclasses with newly created reply data.


#### Required arguments

##### `action`

```python
async def post_reply(
    context: GraphQLContext,
    cleaned_data: PostReplyInput,
) -> Tuple[Thread, Post]:
    ...
```

Next filter or built-in function used to create new reply in the database.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `cleaned_data`

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


### `post_reply_input_hook`

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


#### Required arguments

##### `action`

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


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `validators`

```python
Dict[str, List[AsyncValidator]]
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


### `post_reply_input_model_hook`

```python
post_reply_input_model_hook.call_action(action: PostReplyInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `PostReplyInputModel` GraphQL input type used by the "post reply" GraphQL mutation.

Returns `PostReplyInputModel` input model type.


#### Required arguments

##### `action`

```python
async def create_input_model(context: GraphQLContext) -> PostReplyInputModel:
    ...
```

Next filter or built-in function used to create input model type.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


### `post_thread_hook`

```python
post_thread_hook.call_action(
    action: PostThreadAction,
    context: GraphQLContext,
    cleaned_data: PostThreadInput,
)
```

A filter for the function used by GraphQL mutation creating new thread to create new thread in the database.

Returns tuple of `Thread` and `Post` dataclasses with newly created thread data.


#### Required arguments

##### `action`

```python
async def post_thread(
    context: GraphQLContext,
    cleaned_data: PostThreadInput,
) -> Tuple[Thread, Post]:
    ...
```

Next filter or built-in function used to create new thread in the database.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `cleaned_data`

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


### `post_thread_input_hook`

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


#### Required arguments

##### `action`

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


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `validators`

```python
Dict[str, List[AsyncValidator]]
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


### `post_thread_input_model_hook`

```python
post_thread_input_model_hook.call_action(action: PostThreadInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `PostThreadInputModel` GraphQL input type used by the "post thread" GraphQL mutation.

Returns `PostThreadInputModel` input model type.


#### Required arguments

##### `action`

```python
async def create_input_model(context: GraphQLContext) -> PostThreadInputModel:
    ...
```

Next filter or built-in function used to create input model type.


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


### `register_user_input_hook`

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


#### Required arguments

##### `action`

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


##### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


##### `validators`

```python
Dict[str, List[AsyncValidator]]
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


### `register_user_input_model_hook`

```python
register_user_input_model_hook.call_action(action: RegisterUserInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `RegisterUserInputModel` GraphQL input type used by the "register new user" GraphQL mutation.

Returns `RegisterUserInputModel` input model type.


#### Required arguments

##### `action`

```python
async def create_input_model(context: GraphQLContext) -> RegisterUserInputModel:
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
    cleaned_data: RegisterUserInput
)
```

A filter for the function used by GraphQL mutation registering new user account to register new user in the database.

Returns `User` dataclass with newly created user data.


#### Required arguments

##### `action`

```python
async def register_user(context: GraphQLContext, cleaned_data: RegisterUserInput) -> User:
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


- - -


### `template_context_hook`

```python
template_context_hook.call_action(action: TemplateContextAction, request: Request)
```

A filter for the function used to create default template context.

Returns `TemplateContext` dict with default template context.


#### Required arguments

##### `action`

```python
async def get_default_context(request: Request) -> TemplateContext:
    ...
```

Next filter or built-in function used to create a template context.


#### `request`

```python
Request
```

An instance of [`Request`](https://www.starlette.io/requests/) representing current HTTP request to application.


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