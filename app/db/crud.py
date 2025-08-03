from app.db import models
from sqlalchemy.orm import Session



def create_session(db: Session):
    session_obj = models.Session()
    db.add(session_obj)
    db.commit()
    db.refresh(session_obj)
    return session_obj.id

def add_message(db: Session, session_id: int, role: str, content: str):
    msg = models.ChatMessage(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()


def get_session_history(db: Session, session_id: int):
    return (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.session_id == session_id)
        .order_by(models.ChatMessage.timestamp.asc())
        .all()
    )



