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