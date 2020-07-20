[English](https://github.com/DessertsLab/Sachima/blob/master/README.md)｜[中文简体](https://github.com/DessertsLab/Sachima/blob/master/README_CN.md)｜[中文繁體](https://github.com/DessertsLab/Sachima/blob/master/README_TC.md)

# Sachima

Sachima is a flexiable framework for data-driven apps. It's a MIT licensed open source project written in python. We creates it because our data-driven requirments changes frequently, and we need data analyst having the ability to change online api and data visulization.

Sachima helps you build apps that looks great and intelligently.

You can use Sachima together with [Superset](https://github.com/apache/incubator-superset), or with [sachima-ui](https://github.com/nocmk2/sachima-ui).


[![build status](https://img.shields.io/travis/DessertsLab/Sachima/master.svg?style=flat-square&logo=travis)](https://travis-ci.com/DessertsLab/Sachima)
[![dependencies](https://img.shields.io/librariesio/github/DessertsLab/Sachima?style=flat-square)](https://libraries.io/search?q=sachima)
[![chat](https://img.shields.io/gitter/room/DessertsLab/Sachima?color=purple&logo=gitter&style=flat-square)](https://gitter.im/sachima-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![github code size](https://img.shields.io/github/languages/code-size/DessertsLab/Sachima?color=pink&style=flat-square)]()
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![commit activity](https://img.shields.io/github/commit-activity/w/DessertsLab/Sachima?style=flat-square)](https://github.com/DessertsLab/Sachima/pulse)
[![doc](https://readthedocs.org/projects/sachima/badge/?version=latest&style=flat-square&color=ff69b4)](http://sachima.readthedocs.io/en/latest/?badge=latest)
[![latest](https://img.shields.io/pypi/v/sachima.svg?style=flat-square&logo=python)](https://pypi.python.org/pypi/sachima/)


Features
------------------------------------

|feature|screen casts|description|
|----|----|----|
|api||Publishing your python codes as a http/rpc api.|
|BI platform intergration||Working with BI platform Superset.|
|Message Sending||Sending your data reports to email or sns.|
|Data Visulization||Working with GrassJelly which is a Data Visulization project.
|command line||Command line tools.|

Getting Started
-----------------------------------
First you should have [python](https://www.python.org/downloads/) and [nodejs](https://nodejs.org/en/download/) installed.
Optionally if you already had a python env and you need a separate environment to run Sachima, you should install [virtualenv](https://pypi.org/project/virtualenv/)

Check your installation by run this in command line

``` shell 
python -V
```

``` shell 
node -v
```
> Sometime you need change python to python3 and pip to pip3.

Install sachima by pip

``` python
pip install -U sachima
```

Check sachima version
``` shell
sachima version
```

Cd into your working dir and init Sachima project with example
``` shell
sachima init
```

Update Sachima to latest version and get latest Waffle which is a Sachima frontend development tool.
``` shell
sachima update
```

Run Sachima dev tools
``` shell
sachima run
```
This will start your sachima dev server and display data in Browser. If you had any problem rerun the last step or ask in [Sachima github issues](https://github.com/DessertsLab/Sachima/issues).


Working with BI platform
-----------------------------------

### Working with superset

- git clone https://github.com/pphszx/incubator-superset.git
- git checkout pp_feat_apitable_0.29_new
- virtualenv -p python3 venv
- source sachima_workspace/bin/activate
- pip install -r requirements.txt

    if you get compile error  remove cchardet==1.0.0 from requirements.txt and run again
    https://stackoverflow.com/questions/52509602/cant-compile-c-program-on-a-mac-after-upgrade-to-mojave

- pip install -r requirements-dev.txt
- pip install -e .
- fabmanager create-admin --app superset

    if you already had sqllite db file  ~/.superset/superset.db   rename it to superset_backup.db

- superset db upgrade
- superset init
- superset load_examples

- cd superset/assets
- yarn
- npm run dev

- cd ../..


- create file  ./venv/bin/superset_config.py

``` json

    APP_NAME = 'My App'

    API_URL_CONFIG = {
        'RPC': 'amqp://rabbitname:rabbitpass@0.0.0.0/vhost',
        'RESTFUL': 'http://0.0.0.0:8008/reports',
        'GRPC': '0.0.0.0:50051',
    }
```


- cd superset
- FLASK_ENV=development flask run -p 8088 --with-threads --reload --debugger
- open browser http://127.0.0.1:8088/login/
- ref:https://github.com/apache/incubator-superset/blob/master/CONTRIBUTING.md#flask-server

### Working with schima-ui(WIP)


