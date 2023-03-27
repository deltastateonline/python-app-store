from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint("Health",__name__, description="Simple Health Check")


@blp.route("/health")
class Health(MethodView):

    def get(self):
        return {"message": "Alive"}
