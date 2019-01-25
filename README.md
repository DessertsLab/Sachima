# Sachima

This is a package for Data Analyst who wants to get capabilities of Data Engineer:
- Publishing your code as a http or rpc api.
- Working with BI platform like Superset.
- Sending your data reports to email or sns.
- Working with GrassJelly which is a Data Visulization project.

## dev env
- git clone https://github.com/pphszx/incubator-superset.git
- git checkout pp_feat_apitable_0.29_new
- virtualenv -p python3 venv
- source venv/bin/activate
- pip install -r requirements.txt
> if you get compile error  remove cchardet==1.0.0 from requirements.txt and run again
https://stackoverflow.com/questions/52509602/cant-compile-c-program-on-a-mac-after-upgrade-to-mojave
- pip install -r requirements-dev.txt
- pip install -e .
- fabmanager create-admin --app superset
> if you already had sqllite db file  ~/.superset/superset.db   rename it to superset_backup.db

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

