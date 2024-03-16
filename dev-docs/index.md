# Misago Developer Reference

This directory contains reference documents for Misago developers.

> **Note:** This documentation is a temporary solution. In future I aim to generate Misago's dev documentation from it's codebase, and use Docusaurus to both version it and make it more attractive to browse.


## Markup parser

Misago's markup syntax, parser and renderers that convert parsed markup into an HTML or other representations are implemented in the `misago.parser` package.

- [Markup parser](./parser/index.md)
- [Markup AST](./parser/ast.md)


## Menus

Some of Misago menus can be extended with additional items from code.

- [Menus reference](./menus.md)


## Notifications

Misago's notifications feature is implemented in the `misago.notifications` package.

- [Notifications reference](./notifications.md)

## Plugins

Misago implements a plugin system that extends [Django's existing application mechanism](https://docs.djangoproject.com/en/4.2/ref/applications/), allowing developers to customize and extend standard features.

- [Plugin guide](./plugins/index.md)
- [Plugin installation](./plugins/index.md#plugin-installation)
- [Hooks guide](./plugins/hooks/index.md)
- [Built-in hook reference](./plugins/hooks/reference.md)
