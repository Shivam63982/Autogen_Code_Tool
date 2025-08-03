# app/init_db.py

from sqlalchemy import create_engine
from app.db.models import Base


DATABASE_URL = "postgresql://postgres:9090@localhost:5432/code_tool_db"

engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created.")

if __name__ == "__main__":
    init_db()
