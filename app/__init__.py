from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/carshop_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app.models import product, user, admin

    # Register controllers (blueprints)
    from app.controllers.product import product_bp
    from app.controllers.admin import admin_bp
    from app.controllers.auth import auth_bp

    app.register_blueprint(product_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')   # <-- important
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
