from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # ✅ Required para gumana ang session at flash
    app.config['SECRET_KEY'] = 'dev'  
    # pwede mong palitan ng mas secure na string, halimbawa:
    # app.config['SECRET_KEY'] = 'my_super_secret_key_123'

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/carshop_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models (Admins + Products only)
    from app.models import product, admin

    # Register controllers (blueprints)
    from app.controllers.product import product_bp
    from app.controllers.admin import admin_bp

    app.register_blueprint(product_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
