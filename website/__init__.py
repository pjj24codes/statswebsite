from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "vdykjbdhsnjskw"
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://statsforschoolssql_prxa_user:7khzbfyelxY6DhO2Tfo9xnqjs9ZOhsVB@dpg-cjvpe1nhdsdc739eea60-a.ohio-postgres.render.com/statsforschoolssql_prxa"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    from .models import Team, Game, BasketballPlayerStats, SoccerPlayerStats

    with app.app_context():
        db.create_all()
    
    return app

