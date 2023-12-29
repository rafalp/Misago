# Built-in hooks reference

This document contains a list of all standard plugin hooks existing in Misago.

Hooks instances are importable from the following Python modules:

- [`misago.oauth2.hooks`](#misago-oauth2-hooks)
- [`misago.permissions.hooks`](#misago-permissions-hooks)
- [`misago.users.hooks`](#misago-users-hooks)


## `misago.oauth2.hooks`

`misago.oauth2.hooks` defines the following hooks:

- [`filter_user_data_hook`](./filter-user-data-hook.md)
- [`validate_user_data_hook`](./validate-user-data-hook.md)


## `misago.permissions.hooks`

`misago.permissions.hooks` defines the following hooks:

- [`copy_group_permissions_hook`](./copy-group-permissions-hook.md)


## `misago.users.hooks`

`misago.users.hooks` defines the following hooks:

- [`create_group_hook`](./create-group-hook.md)
- [`delete_group_hook`](./delete-group-hook.md)
- [`set_default_group_hook`](./set-default-group-hook.md)