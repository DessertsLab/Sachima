from flask import Flask, request
from flask_restful import Resource, Api

from flask_api.api import Services


app = Flask(__name__)
api = Api(app)

aaa = Services['tushare']

# data = aaa.query(
#     'stock_company',
#     exchange='SZSE',
#     fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province'
# )

data = aaa.query(
    'top10_holders',
    ts_code='600104.SH',
    start_date='20170101',
    end_date='20171231'
)
col_width = 1 / len(data.columns)


class HelloWorld(Resource):
    def get(self):
        # return data.to_dict()
        # return list(data.reset_index().rename(columns={'index':'key'}).T.to_dict().values())
        return list(map(lambda x: {
            'title': x,
            'dataIndex': x,
            'key': x,
            # 'width':f'{col_width:.0%}',
            # 'sorter':'(a, b) => a.name.length - b.name.length',
        }, data.columns.tolist()))

    def post(self):

        params = request.get_json()
        print(params)

        return {
            'you send: ': params,
            'itemSelect': {
                'Test1': ['111', 'javascript', 'flutter'],
                'Test2': [1, 2, 3],
                '测试3': ['a', 'b', 'c'],
                '测试4': [1],
                '测试5': [''],
                '测试6': [],
            },
            'columns': list(map(
                lambda x: {
                    'title': x,
                    'dataIndex': x,
                    'key': x,
                    'width': f'{col_width:.0%}'
                },
                data.columns.tolist()
            )),
            'dataSource': list(data.reset_index().rename(
                columns={'index': 'key'}).T.to_dict().values())
        }, 201


class Multi(Resource):
    def get(self, num):
        return {'result': num * 10}


api.add_resource(HelloWorld, '/')
api.add_resource(Multi, '/multi/<int:num>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)