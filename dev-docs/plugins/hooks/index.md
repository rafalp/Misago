# Hooks

Hooks are predefined locations in Misago's code where plugins can inject custom Python functions to execute as part of Misago's standard logic. They are one of multiple extension points implemented by Misago.


## Actions and filters

Hooks come in two flavors: actions and filters.

Actions are extra functions called at a given point in Misago's logic. Functions registered in a hook are executed serially, one after another. Depending on the individual hook, they may be used as event handlers, or they can return values of a predetermined type for later use.

Filters wrap existing Misago functions, allowing them to execute custom code before, after, or instead of the standard one. The last function to be registered in a hook is the first one called.


### Registering function in a hook

To register plugin's function in a hook, use **either** the `append` or `prepend` method:

```python
from misago.oauth2.hooks import filter_user_data_hook


# Append and prepend can be used as decorators
@filter_user_data_hook.append
def plugin_function():
    ...


@filter_user_data_hook.prepend
def plugin_function():
    ...


# And called with function as a argument
filter_user_data_hook.append(plugin_function)

filter_user_data_hook.prepend(plugin_function)
```

In action hooks, prepended functions are guaranteed to be called before the appended ones:

```python
action_hook.append(function_1)
action_hook.prepend(function_2)
action_hook.append(function_3)
action_hook.prepend(function_4)

action_hook()
```

In the above example, functions `function_2` and `function_4` will always be called before `function_1` and `function_3`.

Because filter hooks stack their function calls, appended functions are in the lower part of the stack (closer to the wrapped function), while prepended functions are in the top part of the stack (further from the wrapped function):

```python
filter_hook.append(function_1)
filter_hook.prepend(function_2)
filter_hook.append(function_3)
filter_hook.prepend(function_4)

filter_hook()
```

In the above example, functions `function_2` and `function_4` will always be called before `function_1` and `function_3`.

Hooks provide no other guarantees regarding the order of execution of registered functions. This order may change on docker image rebuild or server restart.


## Built-in hooks reference

The list of available hooks, generated from Misago's source code, is available here:

[Built-in hooks reference](./reference.md)

> **The list of hooks is always growing**
> 
> If you have a proposal for a new hook, please post it on the [Misago forums](https://misago-project.org/c/development/31/).


## Implementing custom hooks

There's a dedicated developer guide for implementing a new hook of each type:

- [Implementing an action hook](./action-hook.md)
- [Implementing a filter hook](./filter-hook.md)
