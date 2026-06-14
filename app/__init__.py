from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Two separate SQLAlchemy instances
db_user = SQLAlchemy()
db_admin = SQLAlchemy()

migrate_user = Migrate()
migrate_admin = Migrate()

def create_app():
    app = Flask(__name__)

    # User database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/carshop_db'
    db_user.init_app(app)
    migrate_user.init_app(app, db_user)

    # Admin database (separate URI)
    app.config['SQLALCHEMY_DATABASE_ADMIN_URI'] = 'mysql+pymysql://root:@localhost/admin_db'
    db_admin.init_app(app)
    migrate_admin.init_app(app, db_admin)

    # Import models so migrations can detect them
    from app.models import product
    from app.models_admin import admin_product

    # Register controllers
    from app.controllers.product import product_bp
    from app.controllers.admin import admin_bp
    app.register_blueprint(product_bp)
    app.register_blueprint(admin_bp)

    return app
