#!/usr/bin/env python
import os
import click
import random

import sys
from sachima.sachima_http_server_flask import app
import subprocess
import pkg_resources

sachima_version = pkg_resources.require("sachima")[0].version

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

# sachima_config_file =


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

Better Data Analysis                  version {} 
********************************************************
    """.format(
        sachima_version
    )
    click.echo(random.choice(list(COLORS.values())) + logo)


def is_in_sachima_project():
    if os.path.isfile(os.path.join(os.getcwd(), "./sachima_config.py")):
        click.echo(
            "Your should cd into your sachima project before getting middleware. Maybe you want to create your project first by running sachima init"
        )
        return True
    return False


@click.command(help="Print sachima version")
def version():
    click.echo(sachima_version)


@click.command(help="Get sachima middleware from github : get DessertsLab/pivot_table")
@click.option(
    "--path", default=os.path.join(os.getcwd(), "/middleware"), help="project path"
)
@click.argument("middleware_name")
def get(path, middleware_name):
    if not is_in_sachima_project():
        return
    if not os.path.exists(path):
        os.makedirs(path)
    click.echo(
        "Getting middleware from https://github.com/{} and save to {}".format(
            middleware_name, path
        )
    )
    os.system(
        "git clone https://github.com/{} {}".format(
            middleware_name, os.path.join(path, middleware_name)
        )
    )


@click.command(help="Init a sachima project")
def init():
    click.echo("get something")
    # os.system("git clone https://github.com/{} middleware".format(middleware))


@click.command(help="Start sachima server")
def start():
    click.echo("start sachima server")
    # os.system("git clone https://github.com/{} middleware".format(middleware))


def sync_waffle_and_sachima():
    """
    DessertsLab/Waffle is frontend for sachima dev env
    pre download Waffle from github to the parent dir
    or update Waffle and Sachima 
    """
    WAFFLE_DIR = os.path.join(
        os.getcwd(),
        "..",
        "Waffle",
    )
    if not os.path.exists(WAFFLE_DIR):
        os.system(
            "git clone https://github.com/DessertsLab/Waffle.git {}".format(WAFFLE_DIR)
        )
        os.system("npm install --prefix {}".format(WAFFLE_DIR))
        # 更新sachima到最新版本
        os.system("pip install -U --no-cache-dir sachima")
    else:
        os.system("git -C {0} pull origin master".format(WAFFLE_DIR))
        os.system("pip install -U --no-cache-dir sachima")


def start_sachima():
    sys.dont_write_bytecode = True
    app.run(host="0.0.0.0", port=80, debug=True)


@click.command(help="Run sachima dev server Waffle")
def run():
    if not is_in_sachima_project():
        return
    sync_waffle_and_sachima()

    # --prefix means start npm in a different directory
    cmd_line = "npm start --prefix {0}".format(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Waffle")
    )

    w = subprocess.Popen(
        cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    s = subprocess.Popen(
        start_sachima(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )

    w.wait()
    s.wait()


sachima.add_command(get)
sachima.add_command(init)
sachima.add_command(start)
sachima.add_command(run)
sachima.add_command(version)


if __name__ == "__main__":
    sachima()
