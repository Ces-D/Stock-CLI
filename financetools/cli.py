import os

import click

cmd_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "commands"))

class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"financetools.commands.cmd_{name}", None, None,
                             ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(cls=ComplexCLI)
def cli():
    """A financial tools command line interface."""
    pass