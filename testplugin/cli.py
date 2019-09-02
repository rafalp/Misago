import click

from misago.cli import cli


@cli.add_command
@click.command()
def plugin_command():
    click.echo("HELLO FROM PLUGIN")
