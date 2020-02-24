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

class Account_Balance(Resource):

    # to view balance of a specific account
    def get(self, account_id):
        if (account_id not in list(accounts.keys())):
            return {'status':'Account not found'}
        result = {account_id: accounts[account_id]}
        return jsonify(result)

    # to add or edit an account
    def put(self, account_id):
        name = request.json["name"]
        balance = request.json["balance"]
        if (type(balance) != int) or (balance < 0):
            return {'status':'Not a valid balance amount'}
        accounts[account_id] = {}
        accounts[account_id]['name'] = name
        accounts[account_id]['balance'] = balance
        return {'status':'success',
                'new balance':accounts[account_id]['balance']}

    # delete an account
    def delete(self, account_id):
        del accounts[account_id]
        return {'status':'success'}

class Account_Transfer(Resource):

    # to transfer funds from one account to another account
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
            if (type(amount) != int) or (amount < 0):
                return {'status':'Not a valid transfer amount'}
            accounts[id1]['balance'] -= amount
            accounts[id2]['balance'] += amount

        return {'status':'success'}

# URL paths
api.add_resource(Accounts, '/accounts')
api.add_resource(Account_Balance, '/accounts/<account_id>')
api.add_resource(Account_Transfer, '/accounts/transfer')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)
