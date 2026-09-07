import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:sua_senha@localhost:5432/pill_alarm")
    SQLALCHEMY_TRACK_MODIFICATIONS = False