# create_admin.py

from db.database import SessionLocal
from db.models import User
from passlib.context import CryptContext
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

def create_first_admin():
    email = "admin@edps.com"
    password = "Admin1234"

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print("⚠️ Admin already exists:", email)
        return

    hashed_password = pwd_context.hash(password)
    admin = User(
        email=email,
        hashed_password=hashed_password,
        first_name="Andrew",
        last_name="Hyde",
        role="admin",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        token_version=0
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)
    print("✅ Created admin:", admin.email)

if __name__ == "__main__":
    create_first_admin()
