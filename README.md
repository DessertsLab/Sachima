# Sachima

[English](https://github.com/DessertsLab/Sachima/blob/master/README.md)｜[中文简体](https://github.com/DessertsLab/Sachima/blob/master/README_CN.md)｜[中文繁體](https://github.com/DessertsLab/Sachima/blob/master/README_TC.md)

Sachima is a flexiable framework for data-driven apps.

It helps you build apps that looks great and intelligently.

You can use Sachima together with [Superset](https://github.com/apache/incubator-superset), or with [sachima-ui](https://github.com/nocmk2/sachima-ui).



[![build status](https://img.shields.io/travis/DessertsLab/Sachima/master.svg?style=flat-square&logo=travis)](https://travis-ci.com/DessertsLab/Sachima)
[![dependencies](https://img.shields.io/librariesio/github/DessertsLab/Sachima?style=flat-square)](https://libraries.io/search?q=sachima)
[![chat](https://img.shields.io/gitter/room/DessertsLab/Sachima?color=purple&logo=gitter&style=flat-square)](https://gitter.im/sachima-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![github code size](https://img.shields.io/github/languages/code-size/DessertsLab/Sachima?color=pink&style=flat-square)]()
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![commit activity](https://img.shields.io/github/commit-activity/w/DessertsLab/Sachima?style=flat-square)](https://github.com/DessertsLab/Sachima/pulse)
[![doc](https://readthedocs.org/projects/sachima/badge/?version=latest&style=flat-square&color=ff69b4)](http://sachima.readthedocs.io/en/latest/?badge=latest)
[![latest](https://img.shields.io/pypi/v/sachima.svg?style=flat-square&logo=python)](https://pypi.python.org/pypi/sachima/)


Sachima is a package for Data Analyst:

- Publishing your python codes as a http/rpc api.
- Working with BI platform Superset.
- Sending your data reports to email or sns.
- Working with GrassJelly which is a Data Visulization project.

Getting Started
-----------------------------------
First you should have python3(https://www.python.org/downloads/) and nodejs(https://nodejs.org/en/download/) installed on your os

you should check your installation by

``python3 -V``

.. code::

    Python 3.7.2

``node -v``

.. code::

    v11.6.0




then you will need a separate environment to run Sachima, cd to your working dir and run commands
``pip3 install virtualenv``

``mkdir sachima_start``

``python3 -m venv sachima_start/venv``

``source sachima_start/venv/bin/activate``

``pip3 install sachima``

``sachima init```

``sachima run``

...


``deactivate``



Installation
-----------------------------------
``pip3 install sachima``


Working with superset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

.. code:: json

    APP_NAME = 'My App'

    API_URL_CONFIG = {
        'RPC': 'amqp://rabbitname:rabbitpass@0.0.0.0/vhost',
        'RESTFUL': 'http://0.0.0.0:8008/reports',
        'GRPC': '0.0.0.0:50051',
    }


- cd superset
- FLASK_ENV=development flask run -p 8088 --with-threads --reload --debugger
- open browser http://127.0.0.1:8088/login/
- ref:https://github.com/apache/incubator-superset/blob/master/CONTRIBUTING.md#flask-server



