from app import db


class MedicationLog(db.Model):
    __tablename__ = "medication_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    medication_id = db.Column(
        db.Integer,
        db.ForeignKey("medications.id", ondelete="CASCADE"),
        nullable=False
    )

    scheduled_at = db.Column(
        db.DateTime,
        nullable=False
    )

    taken_at = db.Column(
        db.DateTime
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    medication = db.relationship(
        "Medication",
        back_populates="logs"
    )