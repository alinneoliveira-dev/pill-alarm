from datetime import datetime, timedelta

from flask import Blueprint
from sqlalchemy import text

from app import db


reminders_bp = Blueprint("reminders", __name__)


@reminders_bp.route("/reminders/pending", methods=["GET"])
def pending_reminders():

    now = datetime.now()

    current_time = now.time().replace(
        second=0,
        microsecond=0
    )

    next_minute = (
        datetime.combine(now.date(), current_time)
        + timedelta(minutes=1)
    ).time()

    query = text("""
        SELECT
            ms.id AS schedule_id,
            u.id AS user_id,
            u.name AS user_name,
            u.phone,
            m.id AS medication_id,
            m.name AS medication_name,
            m.dosage,
            ms.time
        FROM medication_schedules ms

        JOIN medications m
            ON m.id = ms.medication_id

        JOIN users u
            ON u.id = m.user_id

        WHERE ms.active = TRUE
          AND m.active = TRUE

          AND ms.time >= :current_time
          AND ms.time < :next_minute

          AND NOT EXISTS (
              SELECT 1
              FROM medication_logs ml
              WHERE ml.medication_id = m.id
                AND ml.scheduled_at = :scheduled_at
          )
    """)

    scheduled_at = datetime.combine(
        now.date(),
        current_time
    )

    result = db.session.execute(
        query,
        {
            "current_time": current_time,
            "next_minute": next_minute,
            "scheduled_at": scheduled_at
        }
    )

    reminders = []

    for row in result:
        reminders.append({
            "schedule_id": row.schedule_id,
            "user_id": row.user_id,
            "user_name": row.user_name,
            "phone": row.phone,
            "medication_id": row.medication_id,
            "medication_name": row.medication_name,
            "dosage": row.dosage,
            "time": str(row.time),
            "scheduled_at": scheduled_at.isoformat()
        })

    return {
        "reminders": reminders
    }