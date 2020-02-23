#!/usr/bin/python3
# import required packages
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
from threading import Lock

app = Flask(__name__)
api = Api(app)

# the dictionary of accounts in the bank
accounts = {'1':{'name':'Gowri','balance':5000},
            '2':{'name':'Prathap','balance':500},
            '3':{'name':'Tutu','balance':6070},
            '4':{'name':'Taku','balance':540},
            '5':{'name':'Manju','balance':3400}
            }
# lock to handle concurrency
lock = Lock()

class Accounts(Resource):

    # Retrieve all accounts
    def get(self):
        return accounts

    # Add or update (if the account already exists) an account
    def put(self):

        id = request.json["id"]
        name = request.json["name"]
        balance = request.json["balance"]

        accounts[id] = {}
        accounts[id]['name'] = name
        accounts[id]['balance'] = balance
        return {'status':'success'}

    # delete an account
    def delete(self):
        id = request.json["id"]
        name = request.json["name"]
        del accounts[id]
        return {'status':'success'}

class Account_Balance(Resource):

    # to view balance of a specific account
    def get(self, account_id):
        result = {account_id: accounts[account_id]}
        return jsonify(result)

    # to deposit funds into an account
    def put(self, account_id):
        deposit = request.json["deposit"]
        accounts[account_id]['balance'] += deposit
        return {'status':'success',
                'new balance':accounts[account_id]['balance']}

class Account_Transfer(Resource):

    # to transfer funds from one account to another
    def post(self):

        id1 = request.json["from"]
        id2 = request.json["to"]

        if (id1 not in list(accounts.keys())) or (id2 not in list(accounts.keys())):
            return {'status': 'Account not found'}
        amount = request.json["amount"]

        # lock to handle mutiple threads
        with lock:
            if (amount > accounts[id1]['balance']):
                return {'status': 'Insufficient funds to conduct transfer'}
            accounts[id1]['balance'] -= amount
            accounts[id2]['balance'] += amount

        return {'status':'success'}

# URL paths
api.add_resource(Accounts, '/accounts')
api.add_resource(Account_Balance, '/accounts/<account_id>')
api.add_resource(Account_Transfer, '/accounts/transfer')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)
