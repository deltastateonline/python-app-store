import uuid
from flask import Flask, request
from db import stores, items
from flask_smorest import abort

app = Flask(__name__)
app.debug = True


@app.get('/store')
def get_stores():
    return {'stores': list(stores.values())}


@app.get('/items')
def get_items():
    return {'items': list(items.values())}


@app.post('/store')
def create_store():
    req_d = request.get_json()
    if 'name' in req_d:
        store_id = uuid.uuid4().hex
        new_store = {**req_d, 'id': store_id}
        stores[store_id] = new_store
        return new_store, 201
    return {"message": "bad request"}, 400


@app.post('/item')
def create_item():
    item_data = request.get_json()
    if item_data['store_id'] not in stores:
        return {"message": "Store not found"},404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id":item_id}
    items[item_id] = item

    return item, 201


@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError as ex:
        return {"message": "Store Not Found.", "ex": ex}, 404


@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError as ex:
        abort(404, message="Item Not Found.")
