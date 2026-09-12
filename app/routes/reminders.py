from datetime import datetime, timedelta

from flask import Blueprint
from sqlalchemy import text

from app import db


reminders_bp = Blueprint("reminders", __name__)


@reminders_bp.route("/reminders/pending", methods=["GET"])
def pending_reminders():

    now = datetime.now()

    current_minute = now.replace(
        second=0,
        microsecond=0
    )

    window_start = current_minute - timedelta(minutes=2)
    window_end = current_minute + timedelta(minutes=1)

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
          AND (
              ms.time >= CAST(:window_start AS TIME)
              OR ms.time < CAST(:window_end AS TIME)
          )
          AND NOT EXISTS (
              SELECT 1
              FROM medication_logs ml
              WHERE ml.medication_id = m.id
                AND ml.scheduled_at >= :window_start
                AND ml.scheduled_at < :window_end
          )
        ORDER BY ms.time
    """)

    result = db.session.execute(
        query,
        {
            "window_start": window_start,
            "window_end": window_end
        }
    )

    reminders = []

    for row in result:

        scheduled_at = datetime.combine(
            current_minute.date(),
            row.time
        )

        if scheduled_at > current_minute:
            scheduled_at -= timedelta(days=1)

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