import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import Storeschema
from sqlalchemy.exc import SQLAlchemyError , IntegrityError
from db import db

from models import  StoreModel

blp = Blueprint("stores",__name__, description="Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, Storeschema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store Deleted"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, Storeschema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(Storeschema)
    @blp.response(200, Storeschema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occured while creating a store.")

        return store
