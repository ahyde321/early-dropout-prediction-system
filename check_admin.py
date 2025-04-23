from db.database import SessionLocal
from db.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

def check_admin():
    # Try to find the admin user
    admin = db.query(User).filter(User.email == "admin@edps.com").first()
    
    if not admin:
        print("❌ No admin user found in database!")
        return
        
    print("✅ Found admin user:")
    print(f"Email: {admin.email}")
    print(f"Role: {admin.role}")
    
    # Test password verification
    test_password = "Admin1234"
    is_valid = pwd_context.verify(test_password, admin.hashed_password)
    print(f"\nTesting password verification:")
    print(f"Password valid: {'✅ Yes' if is_valid else '❌ No'}")
    
    if not is_valid:
        # Create new password hash for comparison
        new_hash = pwd_context.hash(test_password)
        print(f"\nDebug info:")
        print(f"Stored hash: {admin.hashed_password}")
        print(f"Test hash:   {new_hash}")

if __name__ == "__main__":
    check_admin() 