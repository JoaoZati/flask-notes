from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '6ETfzqQUF3d5X9r5EMnLqpANpSqM9tLKFhUX62fazC'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
