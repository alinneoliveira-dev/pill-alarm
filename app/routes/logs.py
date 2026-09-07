from datetime import datetime

from flask import Blueprint, request

from app import db
from app.models import MedicationLog


logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/medication-logs", methods=["POST"])
def create_medication_log():

    data = request.get_json()

    log = MedicationLog(
        medication_id=data["medication_id"],
        scheduled_at=datetime.fromisoformat(
            data["scheduled_at"]
        ),
        status="pending"
    )

    db.session.add(log)
    db.session.commit()

    return {
        "message": "log de medicação criada com sucesso",
        "log": {
            "id": log.id,
            "medication_id": log.medication_id,
            "scheduled_at": log.scheduled_at.isoformat(),
            "taken_at": (
                log.taken_at.isoformat()
                if log.taken_at
                else None
            ),
            "status": log.status
        }
    }, 201