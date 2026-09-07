from app import db


class Medication(db.Model):
    __tablename__ = "medications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    dosage = db.Column(
        db.String(50)
    )

    instructions = db.Column(
        db.Text
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    user = db.relationship(
        "User",
        back_populates="medications"
    )

    schedules = db.relationship(
        "MedicationSchedule",
        back_populates="medication",
        cascade="all, delete-orphan"
    )

    logs = db.relationship(
        "MedicationLog",
        back_populates="medication",
        cascade="all, delete-orphan"
    )