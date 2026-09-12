from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User


users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"])
def create_user():

    data = request.get_json(silent=True)

    if not data:
        return {
            "message": "corpo da requisição inválido"
        }, 400

    name = data.get("name")
    phone = data.get("phone")

    if not name or not phone:
        return {
            "message": "name e phone são obrigatórios"
        }, 400

    name = name.strip()
    phone = phone.strip()

    if not name or not phone:
        return {
            "message": "name e phone não podem estar vazios"
        }, 400

    user = User(
        name=name,
        phone=phone
    )

    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return {
            "message": "já existe um usuário com este telefone"
        }, 409

    return {
        "message": "usuário criado com sucesso",
        "user": {
            "id": user.id,
            "name": user.name,
            "phone": user.phone
        }
    }, 201