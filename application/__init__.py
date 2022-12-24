from flask import Flask
import mysql.connector

class MysqlDB():
    def __init__(self):
        self.cnn = None
    
    def init_app(self, app):
        self.cnn = mysql.connector.connect(
            pool_name = 'mypool',
            pool_size = 5,
            user = app.config['MYSQL_USER'],
            password = app.config['MYSQL_PASSWORD'],
            host = app.config['MYSQL_HOST'],
            database = app.config['MYSQL_DATABASE'])


def init_app():
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize Plugins
    mysql_db.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import api
        from . import views
        # from . import admin

        # # Register Blueprints
        app.register_blueprint(views.view_bp)
        app.register_blueprint(api.api_bp, url_prefix = '/api')

        return app

mysql_db = MysqlDB()