#!/usr/bin/env python
import os
import click

@click.command()
@click.option('get', help="get sachima middleware from github. example: sachima get DessertsLab/pivot_table")
def sachima(middleware):
    os.system("git clone https://github.com/{} middleware".format(middleware))
