.. image:: https://github.com/DessertsLab/assets/blob/master/png/sachima_logo.png 
    :alt: Sachima | LOGO.


Sachima | Better data analyst 
=============================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - Build
      - | |Build Status| |Codecov|
    * - Docs
      - | |Documentation|
    * - Package
      - | |PyPI| |PyPI version| |Wheel| |Supported implementations| |Code style black|
    * - Support
      - | |Wechat| |Join the chat at https://gitter.im/sachima-python/community|

.. |Wechat| image:: https://img.shields.io/badge/wechat-sachima-7bb321.svg?style=popout-square?logo=wechat
   :target: https://community.sanicframework.org/
.. |Join the chat at https://gitter.im/sachima-python/community| image:: https://badges.gitter.im/sachima-python/community.svg
   :target: https://gitter.im/sachima-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |Codecov| image:: https://codecov.io/gh/huge-success/sanic/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/huge-success/sanic
.. |Build Status| image:: https://travis-ci.org/huge-success/sanic.svg?branch=master
   :target: https://travis-ci.org/huge-success/sanic
.. |Documentation| image:: https://readthedocs.org/projects/sanic/badge/?version=latest
   :target: http://sanic.readthedocs.io/en/latest/?badge=latest
.. |PyPI| image:: https://img.shields.io/pypi/v/sanic.svg
   :target: https://pypi.python.org/pypi/sanic/
.. |PyPI version| image:: https://img.shields.io/pypi/pyversions/sanic.svg
   :target: https://pypi.python.org/pypi/sanic/
.. |Code style black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=popout-square
    :target: https://github.com/ambv/black

.. image:: https://badges.gitter.im/sachima-python/community.svg
   :alt: Join the chat at https://gitter.im/sachima-python/community
   :target: https://gitter.im/sachima-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. end-badges


Sachima is a package for Data Analyst who wants to get capabilities of Data Engineer:

- Publishing your code as a http or rpc api.
- Working with BI platform like Superset.
- Sending your data reports to email or sns.
- Working with GrassJelly which is a Data Visulization project.

Installation
---------------------------------
``pip3 install sachima``


Get 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- git clone https://github.com/pphszx/incubator-superset.git
- git checkout pp_feat_apitable_0.29_new
- virtualenv -p python3 venv
- source venv/bin/activate
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



