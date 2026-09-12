from flask import Blueprint, request, render_template

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


@medications_bp.route("/medications", methods=["GET"])
def get_medications():

    medications = Medication.query.filter_by(
        active=True
    ).all()

    result = []

    for medication in medications:

        schedules = []

        for schedule in medication.schedules:

            if schedule.active:
                schedules.append(
                    schedule.time.strftime("%H:%M")
                )

        result.append({
            "id": medication.id,
            "user_id": medication.user_id,
            "name": medication.name,
            "dosage": medication.dosage,
            "instructions": medication.instructions,
            "active": medication.active,
            "schedules": schedules
        })

    return {
        "medications": result
    }, 200


@medications_bp.route(
    "/medications/<int:medication_id>",
    methods=["GET"]
)
def get_medication(medication_id):

    medication = db.session.get(
        Medication,
        medication_id
    )

    if not medication:
        return {
            "message": "medicação não encontrada"
        }, 404

    schedules = []

    for schedule in medication.schedules:

        if schedule.active:
            schedules.append(
                {
                    "id": schedule.id,
                    "time": schedule.time.strftime("%H:%M")
                }
            )

    return {
        "id": medication.id,
        "user_id": medication.user_id,
        "name": medication.name,
        "dosage": medication.dosage,
        "instructions": medication.instructions,
        "active": medication.active,
        "schedules": schedules
    }, 200


@medications_bp.route(
    "/medications/<int:medication_id>",
    methods=["PUT"]
)
def update_medication(medication_id):

    medication = db.session.get(
        Medication,
        medication_id
    )

    if not medication:
        return {
            "message": "medicação não encontrada"
        }, 404

    data = request.get_json(silent=True)

    if not data:
        return {
            "message": "corpo da requisição inválido"
        }, 400

    name = data.get("name")
    dosage = data.get("dosage")
    instructions = data.get("instructions")

    if not isinstance(name, str) or not name.strip():
        return {
            "message": "name não pode estar vazio"
        }, 400

    medication.name = name.strip()

    medication.dosage = (
        dosage.strip()
        if isinstance(dosage, str) and dosage.strip()
        else None
    )

    medication.instructions = (
        instructions.strip()
        if isinstance(instructions, str) and instructions.strip()
        else None
    )

    db.session.commit()

    return {
        "message": "medicação atualizada com sucesso",
        "medication": {
            "id": medication.id,
            "user_id": medication.user_id,
            "name": medication.name,
            "dosage": medication.dosage,
            "instructions": medication.instructions,
            "active": medication.active
        }
    }, 200


@medications_bp.route(
    "/medications/new",
    methods=["GET"]
)
def new_medication():

    return render_template(
        "medication-form.html"
    )


@medications_bp.route(
    "/medications/<int:medication_id>/edit",
    methods=["GET"]
)
def edit_medication(medication_id):

    medication = db.session.get(
        Medication,
        medication_id
    )

    if not medication:
        return {
            "message": "medicação não encontrada"
        }, 404

    return render_template(
        "medication-form.html",
        medication_id=medication_id,
        edit_mode=True
    )


@medications_bp.route(
    "/medications/<int:medication_id>",
    methods=["DELETE"]
)
def delete_medication(medication_id):

    medication = db.session.get(
        Medication,
        medication_id
    )

    if not medication:

        return {
            "message": "medicação não encontrada"
        }, 404

    db.session.delete(medication)
    db.session.commit()

    return {
        "message": "medicação excluída com sucesso"
    }, 200