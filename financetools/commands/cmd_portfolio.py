import click
import os
import json

from financetools.utilities.portfolio_util import AlphaVantageHandler
from financetools.config import ALPHA_VANTAGE_KEY


class Portfolio:
    def __init__(self, api_key):
        self.api = AlphaVantageHandler(api_key=api_key)
        self.portfolio_path = os.fspath(path='financetools\lib\portfolio.json')


@click.group()
@click.pass_context
def cli(ctx):
    """Stock Information"""
    ctx.obj = Portfolio(ALPHA_VANTAGE_KEY)


@cli.command()
@click.pass_context
def list(ctx):
    portfolio_path = open(ctx.obj.portfolio_path)
    portfolio = json.load(portfolio_path)
    click.echo(portfolio["stocks"])


@cli.command()
@click.option('--func', default="GLOBAL_QUOTE", help="Alpha Vantage Endpoint")
@click.option('--symbol', help="Symbol of a Stock")
@click.pass_context
def request(ctx, func, symbol):
    api = ctx.obj.api
    r = api.make_request(func, symbol)
    click.echo(r)
