.. image:: https://github.com/DessertsLab/assets/blob/master/png/sachima_logo.png
    :alt: Sachima | LOGO


Sachima | Better data analyst 
==============================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - Build
      - | |Build Status| |Codecov|
    * - Docs
      - | |Documentation|
    * - Package
      - | |PyPI| |PyPI version| |Code style black|
    * - Support
      - | |Join the chat at https://gitter.im/sachima-python/community|

.. |Build Status| image:: https://travis-ci.com/DessertsLab/Sachima.svg?branch=master
    :target: https://travis-ci.com/DessertsLab/Sachima
.. |Codecov| image:: https://codecov.io/gh/DessertsLab/Sachima/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/DessertsLab/Sachima
.. |Join the chat at https://gitter.im/sachima-python/community| image:: https://badges.gitter.im/sachima-python/community.svg
   :target: https://gitter.im/sachima-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |Documentation| image:: https://readthedocs.org/projects/sachima/badge/?version=latest
   :target: http://sachima.readthedocs.io/en/latest/?badge=latest
.. |PyPI| image:: https://img.shields.io/pypi/v/sachima.svg
   :target: https://pypi.python.org/pypi/sachima/
.. |PyPI version| image:: https://img.shields.io/pypi/pyversions/sachima.svg?logo=python
   :target: https://pypi.python.org/pypi/sachima/
.. |Code style black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. end-badges


Sachima is a package for Data Analyst who wants to get capabilities of Data Engineer:

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



