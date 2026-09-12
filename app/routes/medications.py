from flask import Blueprint, request

from app import db
from app.models import Medication, User


medications_bp = Blueprint("medications", __name__)


@medications_bp.route("/medications", methods=["POST"])
def create_medication():

    data = request.get_json(silent=True)

    if not data:
        return {
            "message": "corpo da requisição inválido"
        }, 400

    if "user_id" not in data or "name" not in data:
        return {
            "message": "user_id e name são obrigatórios"
        }, 400

    try:
        user_id = int(data["user_id"])
    except (TypeError, ValueError):
        return {
            "message": "user_id deve ser um número inteiro"
        }, 400

    name = data["name"]

    if not isinstance(name, str) or not name.strip():
        return {
            "message": "name não pode estar vazio"
        }, 400

    user = db.session.get(User, user_id)

    if not user:
        return {
            "message": "usuário não encontrado"
        }, 404

    medication = Medication(
        user_id=user_id,
        name=name.strip(),
        dosage=data.get("dosage"),
        instructions=data.get("instructions")
    )

    db.session.add(medication)
    db.session.commit()

    return {
        "message": "medicação criada com sucesso",
        "medication": {
            "id": medication.id,
            "user_id": medication.user_id,
            "name": medication.name,
            "dosage": medication.dosage,
            "instructions": medication.instructions,
            "active": medication.active
        }
    }, 201