from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# import libraries for grabbing environment variables
from dotenv import load_dotenv
# used to read environment variables
import os

# gives use access to database operations
db = SQLAlchemy()
migrate = Migrate()

# load values from our .env file so os module can see them
load_dotenv()

def create_app(test_config = None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    # set up database
    if not test_config:
        # development environment config
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("RENDER_DATABASE_URI")
    else:
        # test environment config 
        app.config["TESTING"] = True 
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    # connect database and migrate to our flask app
    db.init_app(app)
    migrate.init_app(app, db)

    # import routes
    from.crystal_routes import crystal_bp
    from.healer_routes import healers_bp
    #register blueprint
    app.register_blueprint(crystal_bp)
    app.register_blueprint(healers_bp)
    #imports model to app
    from app.models.crystal import Crystal

    return app