from flask import Blueprint, request

from app import db
from app.models import User


users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    user = User(
        name=data["name"],
        phone=data["phone"]
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "usuario criado com sucesso",
        "user": {
            "id": user.id,
            "name": user.name,
            "phone": user.phone
        }
    }, 201