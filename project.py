#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)

accounts = {'1':{'name':'Gowri','balance':5000},
            '2':{'name':'Prathap','balance':500},
            '3':{'name':'Tutu','balance':6070},
            '4':{'name':'Taku','balance':540},
            '5':{'name':'Manju','balance':3400}
            }


class Accounts(Resource):
    def get(self):
        return accounts

    def put(self):
        id = request.json["id"]
        name = request.json["name"]
        deposit = request.json["deposit"]
        accounts[id][name] = name
        accounts[id][balance] = deposit

    def delete(self):
        id = request.json["id"]
        name = request.json["name"]
        del accounts[id]
        return {'status':'success'}


class Account_Balance(Resource):
    def get(self, account_id):
        result = {account_id: accounts[account_id]}
        return jsonify(result)

    def put(self, account_id):
        deposit = request.json["deposit"]
        accounts[account_id]['balance'] += deposit
        return {'status':'success'}

class Account_Transfer(Resource):
    def put(self):
        id1 = request.json["id1"]
        name1 = request.json["name1"]
        id2 = request.json["id2"]
        name2 = request.json["name2"]
        if (id1 not in list(accounts.keys())) or (id2 not in list(accounts.keys())):
            return {'status': 'Account not found'}
        if (name1 != accounts[id1]["name"] or name2 != accounts[id2]["name"]):
            return {'status': 'ID and name do not match'}
        transfer = request.json["transfer"]
        if (transfer > accounts[id1]['balance']):
            return {'status': 'Insufficient funds to conduct money transfer'}
        accounts[id1]['balance'] -= transfer
        accounts[id2]['balance'] += transfer
        return {'status':'success'}


api.add_resource(Accounts, '/accounts') # Route_1
api.add_resource(Account_Balance, '/accounts/<account_id>') # Route_3
api.add_resource(Account_Transfer, '/accounts/transfer')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)
