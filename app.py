import os
from flask import Flask,jsonify
from flask_smorest import Api

from db import  db
from blocklist import BLOCKLIST
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from resources.health import blp as HealthBlueprint
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "Stores Rest Api."
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_URL_PREFIX'] = "/"
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
    app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)
    app.config["JWT_SECRET_KEY"] = "SomeSecretKey"

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    #message to return
    @jwt.revoked_token_loader
    def revoke_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description": "Token has been revoked", "error":"token_revoked"})
            , 401
        )

    @jwt.additional_claims_loader
    def add_claim_to_jwt(identity):

        if identity["user_id"] == 1:
            return {"is_admin": True}
        else:
            return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message":"The token has expired.","error":"token_expired"}),
            401
        )
    @jwt.invalid_token_loader #takes an error for the function
    def invalid_token_callback(error):
        return (
            jsonify({"description": "Invalid access token.",
                     "error": "authorization_required"}), 401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"description":"Request does not contain an access token.",
                     "error": "authorization_required"}), 401
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_h, jwt_p):
        return(
            jsonify({
                "description": "The token is not fresh",
                "error": "fresh_token_required"
            }), 401
        )

    # remove this after enabling migrate
    # with app.app_context():
        # db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(HealthBlueprint)
    return app