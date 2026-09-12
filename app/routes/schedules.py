from datetime import datetime

from flask import Blueprint, request

from app import db
from app.models import MedicationSchedule, Medication


schedules_bp = Blueprint("schedules", __name__)


@schedules_bp.route("/schedules", methods=["POST"])
def create_schedule():

    data = request.get_json(silent=True)

    if not data:
        return {
            "message": "corpo da requisição inválido"
        }, 400

    if "medication_id" not in data or "time" not in data:
        return {
            "message": "medication_id e time são obrigatórios"
        }, 400

    try:
        medication_id = int(data["medication_id"])
    except (TypeError, ValueError):
        return {
            "message": "medication_id deve ser um número inteiro"
        }, 400

    try:
        schedule_time = datetime.strptime(
            data["time"],
            "%H:%M:%S"
        ).time()
    except (TypeError, ValueError):
        return {
            "message": "time deve estar no formato HH:MM:SS"
        }, 400

    medication = db.session.get(
        Medication,
        medication_id
    )

    if not medication:
        return {
            "message": "medicação não encontrada"
        }, 404

    schedule = MedicationSchedule(
        medication_id=medication_id,
        time=schedule_time
    )

    db.session.add(schedule)
    db.session.commit()

    return {
        "message": "horário de medicação criado com sucesso",
        "schedule": {
            "id": schedule.id,
            "medication_id": schedule.medication_id,
            "time": schedule.time.strftime("%H:%M:%S"),
            "active": schedule.active
        }
    }, 201