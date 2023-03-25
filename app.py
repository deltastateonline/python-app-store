from flask import Flask, request

app = Flask(__name__)
app.debug = True

stores = [
    {
        "name": "Store 1",
        "items": [
            {
                "name":"chair",
                "price": 15
            }
        ]
    }
]


@app.get('/store')
def get_stores():
    return {'stores': stores}


@app.post('/store')
def create_store():
    req_d = request.get_json()
    if  'name' in req_d:
        new_store = {"name": req_d["name"], "items": []}
        stores.append(new_store)
        return new_store, 201
    return {"message": "bad request"}, 400


@app.post('/store/<string:name>/item')
def create_item(name):
    req_d = request.get_json()
    for a_store in stores:
        if a_store["name"] == name:
            new_item = {
                "name": req_d["name"],
                "price": req_d["price"]
            }
            a_store["items"].append(new_item)
            return new_item, 201

    return {"message": "Store Not Found."}, 400


@app.get('/store/<string:name>')
def get_store(name):
    req_d = request.get_json()
    for a_store in stores:
        if a_store["name"] == name:
            return {"items": a_store['items']}, 200

    return {"message": "Store Not Found."}, 400
