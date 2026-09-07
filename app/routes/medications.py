from flask import Blueprint, request
from app import db
from app.models import Medication

medications_bp = Blueprint("medications", __name__)


@medications_bp.route("/medications", methods=["POST"])
def create_medication():
    data = request.get_json()

    medication = Medication(
        user_id=data["user_id"],
        name=data["name"],
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
            "instructions": medication.instructions
        }
    }, 201