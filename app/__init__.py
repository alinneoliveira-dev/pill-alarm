from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)

    from app.routes.health import health_bp
    app.register_blueprint(health_bp)

    from app.routes.users import users_bp
    app.register_blueprint(users_bp)

    from app.routes.medications import medications_bp
    app.register_blueprint(medications_bp)

    from app.routes.schedules import schedules_bp
    app.register_blueprint(schedules_bp)

    from app.routes.reminders import reminders_bp
    app.register_blueprint(reminders_bp)

    from app.routes.logs import logs_bp
    app.register_blueprint(logs_bp)

    return app