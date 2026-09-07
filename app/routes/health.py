from flask import Blueprint
from sqlalchemy import text

from app import db


health_bp = Blueprint("health", __name__)


@health_bp.route("/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500