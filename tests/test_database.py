# tests/test_database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base  # Assuming you have your Base = declarative_base()
from db.models import Student, RiskPrediction, User, Notification  # Explicitly import all models to ensure they're registered

# In-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables before the tests start
def setup_test_db():
    Base.metadata.drop_all(bind=engine)  # Clear any existing tables
    Base.metadata.create_all(bind=engine)  # Create fresh tables

# Initialize tables
setup_test_db()
