#!/usr/bin/env python
import os
import click
import random

import sys
import subprocess
import pkg_resources
import webbrowser

import shutil

sachima_version = pkg_resources.require("sachima")[0].version
sys.path.insert(0, os.getcwd())

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

CURRENT_DIR = os.getcwd()
WAFFLE_DIR = os.path.join(CURRENT_DIR, "..", "Waffle")


@click.group()
def sachima():
    logo = """
*********************************************************
                _     _                 
               | |   (_)                
 ___  __ _  ___| |__  _ _ __ ___   __ _ 
/ __|/ _` |/ __| '_ \| | '_ ` _ \ / _` |
\__ \ (_| | (__| | | | | | | | | | (_| |
|___/\__,_|\___|_| |_|_|_| |_| |_|\__,_|

Better Data Analysis                  version {} 
*********************************************************
    """.format(
        sachima_version
    )
    click.echo(random.choice(list(COLORS.values())) + logo)


def is_in_sachima_project():
    if os.path.isfile(os.path.join(os.getcwd(), "./sachima_config.py")):
        return True

    click.echo(
        "You should cd into your sachima project. Maybe you want to create your project first by running sachima init"
    )
    return False


def sync_waffle():
    """
    DessertsLab/Waffle is frontend for sachima dev env
    pre download Waffle from github to the parent dir
    or update Waffle 
    """
    if not os.path.exists(WAFFLE_DIR):
        click.echo("Cloneing  DessertsLab/Waffle...")
        os.system(
            "git clone https://github.com/DessertsLab/Waffle.git {}".format(
                WAFFLE_DIR
            )
        )
        click.echo("Installing  DessertsLab/Waffle...")

        # os.system("cd {}".format(WAFFLE_DIR))
        os.chdir(WAFFLE_DIR)
        os.system("npm install")
        os.chdir(CURRENT_DIR)
    else:
        click.echo("Pulling  DessertsLab/Waffle...")
        os.system("git -C {0} pull origin master".format(WAFFLE_DIR))
        click.echo("Installing  DessertsLab/Waffle...")
        os.chdir(WAFFLE_DIR)
        os.system("npm install")
        os.chdir(CURRENT_DIR)


def start_sachima():
    from sachima.sachima_http_server_flask import app

    sys.path.insert(0, os.getcwd())
    sys.dont_write_bytecode = True
    app.run(host="0.0.0.0", port=80, debug=False)


@click.command(help="Print sachima version")
def version():
    click.echo(sachima_version)


@click.command(
    help="Get sachima middleware from github : get DessertsLab/pivot_table"
)
@click.option(
    "--path",
    default=os.path.join(os.getcwd(), "middleware"),
    help="project path",
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
@click.argument("name")
def init(name):
    sachima_example_path = os.path.join(os.path.dirname(__file__), "example")
    current_init_path = os.path.join(os.getcwd(), name)
    click.echo(
        "copying {} to {} ...".format(sachima_example_path, current_init_path)
    )
    shutil.copytree(sachima_example_path, current_init_path)
    click.echo("Init a sachima project successed")


@click.command(
    help="Start sachima dev server with syncing Waffle source code from github(For contributors)"
)
def start():
    click.echo("start sachima dev server")
    if not is_in_sachima_project():
        return
    sync_waffle()
    # --prefix means start npm in a different directory
    cmd_line = "npm start --prefix {0}".format(WAFFLE_DIR)
    w = subprocess.Popen(
        cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    s = subprocess.Popen(
        start_sachima(),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    w.wait()
    s.wait()


@click.command(help="Update sachima")
@click.option("--local", default="", help="if in china use tsinghua source")
def update(local):
    click.echo("Updating sachima...")
    state = 0
    if local == "china":
        state = os.system(
            "pip3 --default-timeout=100 install -U sachima -i https://pypi.tuna.tsinghua.edu.cn/simple"
        )
    else:
        state = os.system("pip3 install -U sachima")

    if state == 0:
        click.echo(
            "Sachima already updated to {}".format(
                pkg_resources.require("sachima")[0].version
            )
        )
        os.system("sachima version")


@click.command(help="Run sachima")
def run():
    if not is_in_sachima_project():
        return
    # Open browser first while sachima backend starting the browser will update automaticly
    url = "http://127.0.0.1:80"
    webbrowser.open_new(url)
    start_sachima()


sachima.add_command(get)
sachima.add_command(init)
sachima.add_command(start)
sachima.add_command(run)
sachima.add_command(version)
sachima.add_command(update)


if __name__ == "__main__":
    sachima()
