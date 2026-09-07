from app import db


class MedicationSchedule(db.Model):
    __tablename__ = "medication_schedules"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    medication_id = db.Column(
        db.Integer,
        db.ForeignKey("medications.id", ondelete="CASCADE"),
        nullable=False
    )

    time = db.Column(
        db.Time,
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    medication = db.relationship(
        "Medication",
        back_populates="schedules"
    )