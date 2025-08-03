from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:9090@localhost:5432/code_tool_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()














#======================================================================================================
# db = SessionLocal()           # Create a DB session
# session = db.query(Session).first()  # Query the first Session row from DB
# all_messages = session.messages 




# This advanced Python project involves building an AI-powered Emergency Response System for a smart city using concepts like graph theory, real-time simulation, machine learning, and REST APIs. The city is modeled as a dynamic weighted graph where intersections are nodes and roads have traffic-based weights that update in real-time using threading or async I/O. Emergency units (ambulances, firetrucks, police) are managed as objects with attributes like location, availability, and speed, and the system uses A* or Dijkstra's algorithm to calculate the fastest path. To optimize response, a machine learning model predicts the best unit to dispatch based on distance, traffic, emergency type, and time of day, while recent route calculations are cached for performance using LRU caching. Optionally, a Flask or FastAPI server exposes endpoints for reporting emergencies and tracking units, enabling full-scale simulation and testing of emergency logistics in a smart city environment. Generate the code to complete the project.