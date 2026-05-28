# db_logger.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Configuration
DATABASE_URL = "sqlite:///agent_log.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database Table Definition
class AgentLog(Base):
    __tablename__ = "agent_log"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    agent_name = Column(String)     
    action_type = Column(String)    # e.g., 'Thought', 'Action', 'Result'
    description = Column(String)    

def create_db_tables():
    """Creates all defined tables in the database if they don't exist."""
    print("--- Initializing Database ---")
    Base.metadata.create_all(bind=engine)
    print("--- Database initialized successfully ---")

def log_agent_action(agent_name: str, action_type: str, description: str):
    """Logs a single action or thought to the database."""
    try:
        db = SessionLocal()
        log_entry = AgentLog(
            agent_name=agent_name,
            action_type=action_type,
            description=description
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        db.close()
        print(f"[DB LOG] {agent_name} | {action_type}: {description[:50]}...")
    except Exception as e:
        print(f"[DB LOG ERROR] Could not log action: {e}")

if __name__ == "__main__":
    create_db_tables()
    log_agent_action("System", "Setup", "Database connection tested successfully.")