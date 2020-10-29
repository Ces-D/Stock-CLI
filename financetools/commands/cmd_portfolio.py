import click
import os
import json
import datetime
import pandas as pd

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
                json.dump(data, write)
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
                json.dump(stocks, write)
            click.echo(f"{s} has been removed from Portfolio")
        else:
            click.echo(f"{s} does not exist in Portfolio")


# @cli.command()
# @click.pass_context
# def update(ctx):
#     with open(ctx.obj.portfolio_path) as read:
#         api = ctx.obj.api
#         file_data = json.load(read)
#         file_update = {"stocks":[]}
#         stock_symbols = [item.get("symbol") for item in file_data["stocks"]]

#         for symbol in stock_symbols:
#             index = stock_symbols.index(symbol)
#             response = api.make_request(symbol).get("Global Quote")
#             stock_item = file_data["stocks"][index]
#             stock_data = stock_item["data"]
#             captured = {
#                 "date": datetime.datetime.today().strftime('%c'),
#                 "open": response["02. open"],
#                 "price": response["05. price"],
#                 "previous_close": response["08. previous close"],
#                 "change": response["09. change"],
#                 "change_percent": response["10. change percent"]
#             }
#             updated_stock_data = stock_data.append(captured)
#             click.echo(updated_stock_data)
#             updated_stock_item = stock_item["data"].append(updated_stock_data)
#             click.echo(updated_stock_item)
#             file_update["stocks"].append(updated_stock_item)
#         click.echo(file_update)
#     # click.echo("Portfolio has been updated")


@cli.command()
@click.pass_context
def update(ctx):
    json_file = pd.read_json(ctx.obj.portfolio_path, typ='series')
    stocks = json_file["stocks"]
    updated = stocks[1]["data"]
    click.echo(updated)
