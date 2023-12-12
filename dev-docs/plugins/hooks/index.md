# Hooks

Hooks are predefined locations in Misago's code where plugins can inject custom Python functions to execute as part of Misago's standard logic. They are one of multiple extension points implemented by Misago.


## Actions and filters

Hooks come in two flavors: actions and filters.

Actions are extra functions called at a given point in Misago's logic. Depending on an individual hook, they may be used as event handlers, or they can return values of a predetermined type for later use. Plugin outlets in Misago's templates are implemented as action hooks

Filters wrap the existing Misago functions. They can execute custom code before, after, or instead of the standard one. Because of how powerful they are, they make up the majority of hooks in Misago's core.


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
