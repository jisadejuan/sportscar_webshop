from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Single SQLAlchemy instance
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Secret key required for sessions and flash messages
    app.config['SECRET_KEY'] = 'dev'  # replace with a strong random key in production

    # Database configuration (single DB)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/carshop_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Flask-Migrate can detect them
    from app.models import product, user, admin_user

    # Register controllers (blueprints)
    from app.controllers.product import product_bp
    from app.controllers.admin import admin_bp
    from app.controllers.auth import auth_bp

    app.register_blueprint(product_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

    return app
