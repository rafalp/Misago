# Plugin guide

Misago implements a plugin system that enables developers to customize and extend the core functionality of the software. This plugin system itself extends existing Django applications mechanism.

> **Plugins vs forking Misago**
>
> It may seem simpler (and faster) to fork and customize Misago directly instead of developing plugins. While this is feasible, the time required to keep the fork in sync with new versions of Misago for every site update may quickly accumulate, resulting in a net loss for your project or site.
>
> It is recommended to attempt achieving as much as possible through plugins. In situations where this is not feasible, consider [reaching out to the developers](https://misago-project.org/c/development/31/) before resorting to forking. Misago's current extension points are not exhaustive, and new ones may be added in future releases based on user feedback.


## Plugin installation


## Writing custom plugin

- django applications mechanism
- plugin structure
- plugins vs. forking


## Hooks

- how to hooks
- hook reference