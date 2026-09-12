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

@logs_bp.route("/medication-logs/take-latest", methods=["POST"])
def take_latest_medication():

    log = MedicationLog.query.filter_by(
        status="pending"
    ).order_by(
        MedicationLog.scheduled_at.desc()
    ).first()

    if not log:
        return {
            "message": "nenhuma medicação pendente encontrada"
        }, 404

    log.status = "taken"
    log.taken_at = datetime.now()

    db.session.commit()

    return {
        "message": "medicação marcada como tomada",
        "log": {
            "id": log.id,
            "medication_id": log.medication_id,
            "scheduled_at": log.scheduled_at.isoformat(),
            "taken_at": log.taken_at.isoformat(),
            "status": log.status
        }
    }, 200

@logs_bp.route("/medication-logs/skip-latest", methods=["POST"])
def skip_latest_medication():

    log = MedicationLog.query.filter_by(
        status="pending"
    ).order_by(
        MedicationLog.scheduled_at.desc()
    ).first()

    if not log:
        return {
            "message": "Nenhuma medicação pendente encontrada"
        }, 404

    log.status = "skipped"

    db.session.commit()

    return {
        "message": "medicação marcada como não tomada",
        "log": {
            "id": log.id,
            "medication_id": log.medication_id,
            "scheduled_at": log.scheduled_at.isoformat(),
            "taken_at": None,
            "status": log.status
        }
    }, 200