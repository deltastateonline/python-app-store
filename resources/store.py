import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores",__name__, description="Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError as ex:
            abort(404, message="Store Not Found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store Deleted."}
        except KeyError as ex:
            abort(404, message="Store Not Found.")


@blp.route("/store")
class StroreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        req_d = request.get_json()
        if 'name' in req_d:
            store_id = uuid.uuid4().hex
            new_store = {**req_d, 'id': store_id}
            stores[store_id] = new_store
            return new_store, 201
        return {"message": "bad request"}, 400
