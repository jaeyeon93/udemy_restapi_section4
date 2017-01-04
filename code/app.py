# -*- coding:utf-8 -*-

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
# resource는 api가 리턴하는 값들?로 생각할 수 있다

app = Flask(__name__)
app.secret_key = 'jaeyeon'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth
# jwt create an new endpoint?

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                            required=True,
                            help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self , name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = next(filter(lambda x: x['name'] == name, items), None)# If next function can't find the item. it returns None
        # filter함수는 첫번째 인수로 함수이름을 두번째인수로는 반복가능한 자료형을 받는다 반복가능한 자료형요소들이 첫번째 인수 함수에 입력됬을때 참값만 리턴한다
        #lambda 인수1 : 표현식
        return {'item': item}, 200 if item else 404


    def post(self,name):
        """parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This field cannot be left blank!"
                            )
        data = parser.parse_args()"""
        #data = request.get_json()
        # If content type is not json, data variable'll give error message,
        # get_json(force=True) means that you do not need content type header but it's dangerous
        # get_json(seilent=True) it doesn't give an error, it gives None


        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': 'An item with name "{}" already exists.'.format(name)}, 400

        data = Item.parser.parse_args() # data가 위에있는것보다 이 위치에 있는게 좋다. 위에 함수에 문제가 있으면 실행이 안된다, data는 로딩데이터이다
        # 이렇게하는게 프로세스에 깔끔하다

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self,name):
        global items # global variable
        items = list(filter(lambda x: x['name'] != name, items))
        # items only exist in delete function, local variable
        return {'message' : 'Item deleted'}

    def put(self, name):
        """parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This field cannot be left blank!"
                            )
        data = parser.parse_args()"""
        #data = request.get_json() parser방법으로 안하고 이렇게해도 된다
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items),None)
        if item is None:
            item = {'name':name, 'price':data['price']}
            item.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items':items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

app.run(port=5000, debug=True)
