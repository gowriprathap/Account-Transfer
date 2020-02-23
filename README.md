# RESTFUL API's for Bank Transfer

1. Written using Python 2.7
2. Flask 1.1
3. No database: Data stored in memory (dictionary)


## How to use the API

### List of all the accounts
1. Method: GET
2. Endpoint: ```http://IP:5000/accounts```

### Get account details
1. Method: GET
2. Endpoint: ```http://IP:5000/accounts/<id>```

### Add or edit an account
1. Method: PUT
2. Endpoint: ```http://IP:5000/accounts/<id>```
3. Body: ```{ "name": "<name>", "balance": <balance> }```

### Delete an account
1. Method: DELETE
2. Endpoint: ```http://IP:5000/accounts/<id>```

### Transfer funds from one account to another
1. Method: POST
2. Endpoint: ```http://IP:5000/accounts/transfer```
3. Body: ```{ "from": "<id1>", "to": "<id2>", amount: <amount> }```
