#!/usr/bin/env python
from misago.cli import cli
from misago.plugins import import_plugins


if __name__ == "__main__":
    import_plugins()
    cli()