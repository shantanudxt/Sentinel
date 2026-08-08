from app.database.connection import engine, Base
from app.database import models


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created")