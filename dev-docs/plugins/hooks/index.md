# Hooks guide

Hooks are predefined locations in Misago's code where plugins can inject custom Python functions to execute as part of Misago's standard logic. They make one of multiple extension points implemented by Misago.


## Actions and filters

Hooks come in two flavors: actions and filters.

Actions are extra functions called at a given point in Misago's logic. Depending on the individual hook, they may be used as event handlers, or they can return values of a predetermined type for later use:

```python
# Action returning a dict with extra forum stat to display somewhere
def plugin_action(request: HttpRequest) -> dict:
    return {"name": "Unapproved threads", "count": count_unapproved_threads()}
```

Filters wrap existing Misago functions, allowing them to execute custom code before, after, or instead of the standard one:

```python
# Filter that wraps standard Misago parse function (an "action")
# with simple bad words censor
def plugin_filter(action: MessageParser, request: HttpRequest, message: str) -> str:
    parsed_message = action(request, message)
    return parsed_message.replace("gamble", "****")
```


### Registering a function in an action hook

To register plugin's function in an action hook, use the `append_action` or `prepend_action` method:

```python
# append_action and prepend_action can be used as decorators
@action_hook.append_action
def plugin_function(...):
    ...


@action_hook.prepend_action
def plugin_function(...):
    ...


# And called with function as an argument
action_hook.append_action(plugin_function)
action_hook.prepend_action(plugin_function)
```

In action hooks, prepended functions are guaranteed to be called before the appended ones:

```python
action_hook.append_action(function_1)
action_hook.prepend_action(function_2)
action_hook.append_action(function_3)
action_hook.prepend_action(function_4)

action_hook()
```

In the above example, functions `function_2` and `function_4` will always be called before `function_1` and `function_3`.


### Registering a function in a filter hook

To register plugin's function in a filter hook, use the `append_filter` or `prepend_filter` method:

```python
# append_filter and prepend_filter can be used as decorators
@filter_hook.append_filter
def plugin_function(...):
    ...


@filter_hook.prepend_filter
def plugin_function(...):
    ...


# And called with function as an argument
filter_hook.append_filter(plugin_function)
filter_hook.prepend_filter(plugin_function)
```

Because filter hooks stack their function calls, appended functions are in the top part of the stack (further from the wrapped function), while prepended functions are in the lower part of the stack (closer to the wrapped function):

```python
filter_hook.append_filter(function_1)
filter_hook.prepend_filter(function_2)
filter_hook.append_filter(function_3)
filter_hook.prepend_filter(function_4)

filter_hook()
```

In the above example, functions `function_1` and `function_3` will always be called before `function_2` and `function_4`.


## Built-in hooks reference

The list of available hooks, generated from Misago's source code, is available here:

[Built-in hooks reference](./reference.md)

> **The list of hooks is always growing**
> 
> If you have a proposal for a new hook, please post it on the [Misago forums](https://misago-project.org/c/development/31/).


## Implementing custom hooks

The following developer guides document the implementation of a new hook for each type:

- [Implementing an action hook](./action-hook.md)
- [Implementing a filter hook](./filter-hook.md)
