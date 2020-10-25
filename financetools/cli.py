import click
from financetools.stock import portfolio

@click.group()

def cli():
    pass

cli.add_command(portfolio)


