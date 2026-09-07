from flask import Blueprint, request
from app import db
from app.models import MedicationSchedule

schedules_bp = Blueprint("schedules", __name__)


@schedules_bp.route("/schedules", methods=["POST"])
def create_schedules():
    data = request.get_json()

    schedule = MedicationSchedule(
        medication_id=data["medication_id"],
        time=data["time"]
    )

    db.session.add(schedule)
    db.session.commit()

    return {
        "message": "medicação criada com sucesso",
        "schedule": {
        "id": schedule.id,
        "medication_id": schedule.medication_id,
        "time": schedule.time.strftime("%H:%M:%S"),
        "active": schedule.active
        }
    }, 201