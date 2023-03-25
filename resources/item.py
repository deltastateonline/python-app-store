import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items


blp = Blueprint("Items",__name__, description="Operation on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError as ex:
            abort(404, message="Item Not Found.")


    def delete(self, item_id):
        try:
            del items[item_id]
            return {"Item Deleted."}
        except KeyError as ex:
            abort(404, message="Item Not Found.")

    def put(self,item_id):
        item_data = request.get_json()
        try:
            item = items[item_id]
            item != item_data
            return item
        except KeyError as ex:
            abort(404, message="Item Not Found.")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if item_data['store_id'] not in stores:
            return {"message": "Store not found"}, 404

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item, 201

