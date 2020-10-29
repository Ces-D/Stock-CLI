import click
import os
import json
import datetime

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
def stocks(ctx):
    portfolio_path = open(ctx.obj.portfolio_path)
    portfolio = json.load(portfolio_path)
    names = [item.get("symbol") for item in portfolio["stocks"]]
    click.echo(names)


@cli.command()
@click.option('--symbol', "-s", help="Symbol of a Stock")
@click.option('--func',
              "-f",
              default="GLOBAL_QUOTE",
              help="Alpha Vantage Endpoint")
@click.pass_context
def lookup(ctx, symbol, func):
    api = ctx.obj.api
    r = api.make_request(symbol, function_name=func)
    click.echo(r)


@cli.command()
@click.option("-s", type=str)
@click.pass_context
def add(ctx, s):
    with open(ctx.obj.portfolio_path) as read:
        data = json.load(read)
        symbols = [item.get("symbol") for item in data["stocks"]]
        if symbols.count(s) > 0:
            click.echo(f"{s} already exists in Portfolio")
        else:
            item = {"symbol": s, "data": []}
            data["stocks"].append(item)
            with open(ctx.obj.portfolio_path, "w") as write:
                json.dump(data, write, indent=4)
            click.echo(f"{s} has been added to Portfolio")


@cli.command()
@click.option("-s", type=str)
@click.pass_context
def remove(ctx, s):
    with open(ctx.obj.portfolio_path) as read:
        data = json.load(read)
        symbols = [item.get("symbol") for item in data["stocks"]]
        if symbols.count(s) > 0:
            items = [
                item for item in data["stocks"]
                if not (s == item.get("symbol"))
            ]
            stocks = {"stocks": items}
            with open(ctx.obj.portfolio_path, "w") as write:
                json.dump(stocks, write, indent=4)
            click.echo(f"{s} has been removed from Portfolio")
        else:
            click.echo(f"{s} does not exist in Portfolio")


@cli.command()
@click.pass_context
def update(ctx):
    with open(ctx.obj.portfolio_path) as json_file:
        data = json.load(json_file)
        stocks = data["stocks"]
        stock_symbols = [item.get("symbol") for item in stocks]
        for symbol in stock_symbols:
            index = stock_symbols.index(symbol)
            location = stocks[index].get("data")
            response = ctx.obj.api.make_request(symbol).get("Global Quote")
            formatted_response = {
                "date": datetime.datetime.now().strftime("%c"),
                "open": response["02. open"],
                "low": response["04. low"],
                "high": response["03. high"],
                "price": response["05. price"],
                "change": response["09. change"],
                "change_percent": response["10. change percent"]
            }
            location.append(formatted_response)
            with open(ctx.obj.portfolio_path, "w") as write_file:
                json.dump(data, write_file, indent=4)
        click.echo("Portfolio has been Updated")
