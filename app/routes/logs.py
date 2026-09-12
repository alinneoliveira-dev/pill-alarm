from datetime import datetime

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import MedicationLog


logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/medication-logs", methods=["POST"])
def create_medication_log():

    data = request.get_json(silent=True)

    if not data:
        return {
            "message": "corpo da requisição inválido"
        }, 400

    if "medication_id" not in data or "scheduled_at" not in data:
        return {
            "message": "medication_id e scheduled_at são obrigatórios"
        }, 400

    try:
        medication_id = int(data["medication_id"])
    except (TypeError, ValueError):
        return {
            "message": "medication_id deve ser um número inteiro"
        }, 400

    try:
        scheduled_at = datetime.fromisoformat(
            data["scheduled_at"]
        )
    except (TypeError, ValueError):
        return {
            "message": "scheduled_at deve estar em formato ISO válido"
        }, 400

    log = MedicationLog(
        medication_id=medication_id,
        scheduled_at=scheduled_at,
        status="pending"
    )

    db.session.add(log)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return {
            "message": "já existe um log para esta medicação neste horário"
        }, 409

    return {
        "message": "log de medicação criada com sucesso",
        "log": {
            "id": log.id,
            "medication_id": log.medication_id,
            "scheduled_at": log.scheduled_at.isoformat(),
            "taken_at": None,
            "status": log.status
        }
    }, 201


@logs_bp.route("/medication-logs/take", methods=["POST"])
def take_medication():

    data = request.get_json(silent=True)

    if not data:
        return {
            "message": "corpo da requisição inválido"
        }, 400

    if "medication_id" not in data or "scheduled_at" not in data:
        return {
            "message": "medication_id e scheduled_at são obrigatórios"
        }, 400

    try:
        medication_id = int(data["medication_id"])
    except (TypeError, ValueError):
        return {
            "message": "medication_id deve ser um número inteiro"
        }, 400

    try:
        scheduled_at = datetime.fromisoformat(
            data["scheduled_at"]
        )
    except (TypeError, ValueError):
        return {
            "message": "scheduled_at deve estar em formato ISO válido"
        }, 400

    log = MedicationLog.query.filter_by(
        medication_id=medication_id,
        scheduled_at=scheduled_at,
        status="pending"
    ).first()

    if not log:
        return {
            "message": "log de medicação pendente não encontrado"
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


@logs_bp.route("/medication-logs/skip", methods=["POST"])
def skip_medication():

    data = request.get_json(silent=True)

    if not data:
        return {
            "message": "corpo da requisição inválido"
        }, 400

    if "medication_id" not in data or "scheduled_at" not in data:
        return {
            "message": "medication_id e scheduled_at são obrigatórios"
        }, 400

    try:
        medication_id = int(data["medication_id"])
    except (TypeError, ValueError):
        return {
            "message": "medication_id deve ser um número inteiro"
        }, 400

    try:
        scheduled_at = datetime.fromisoformat(
            data["scheduled_at"]
        )
    except (TypeError, ValueError):
        return {
            "message": "scheduled_at deve estar em formato ISO válido"
        }, 400

    log = MedicationLog.query.filter_by(
        medication_id=medication_id,
        scheduled_at=scheduled_at,
        status="pending"
    ).first()

    if not log:
        return {
            "message": "log de medicação pendente não encontrado"
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