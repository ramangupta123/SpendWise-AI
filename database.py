from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Create a local SQLite database file named 'expenses.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///expenses.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 2. Setup Session Local for database queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base class for declarative database models
Base = declarative_base()


def get_db():
    """Helper function to open and close DB sessions cleanly."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
