#!/usr/bin/env python
import os
import click
import random

COLORS = {
    "black": "\u001b[30;1m",
    "red": "\u001b[31;1m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33;1m",
    "blue": "\u001b[34;1m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    # "yellow-background":"\u001b[43m",
    # "black-background":"\u001b[40m",
    # "cyan-background":"\u001b[46;1m",
}


@click.group()
def sachima():
    logo = """
********************************************************
                _     _                 
            | |   (_)                
___  __ _  ___| |__  _ _ __ ___   __ _ 
/ __|/ _` |/ __| '_ \| | '_ ` _ \ / _` |
\__ \ (_| | (__| | | | | | | | | | (_| |
|___/\__,_|\___|_| |_|_|_| |_| |_|\__,_|

Better Data Analysis                  version 2020.7.6.3
********************************************************
    """
    click.echo(random.choice(list(COLORS.values())) + logo)


@click.command(help="Get sachima middleware from github : get DessertsLab/pivot_table")
@click.option("--path", default="./", help="project path")
@click.argument("middleware_name")
def get(path, middleware_name):
    click.echo("Get middleware from https://github.com/{} and save to {}".format(middleware_name, path))
    # os.system("git clone https://github.com/{} middleware".format(middleware))


@click.command(help="Init a sachima project")
def init():
    click.echo("get something")
    # os.system("git clone https://github.com/{} middleware".format(middleware))


@click.command(help="Start sachima server")
def start():
    click.echo("start sachima server")
    # os.system("git clone https://github.com/{} middleware".format(middleware))


sachima.add_command(get)
sachima.add_command(init)
sachima.add_command(start)


if __name__ == "__main__":
    sachima()
