#!/usr/bin/env python
"""
Script to create test notifications for users in the system.
Run this script to populate the notification system with sample data.
"""

import os
import sys
from datetime import datetime
from sqlalchemy.orm import Session

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal
from db.models import Notification, User

def create_test_notifications():
    """Create test notifications for all users"""
    db = SessionLocal()
    try:
        # Get all active users
        users = db.query(User).filter(User.is_active == True).all()
        
        if not users:
            print("❌ No active users found. Please create users first.")
            return
        
        print(f"🔍 Found {len(users)} active users")
        
        # Create different types of notifications for each user
        for user in users:
            print(f"📧 Creating notifications for user: {user.email}")
            
            now = datetime.utcnow()
            
            # Info notification
            info_notification = Notification(
                user_id=user.id,
                title="Welcome to EDPS",
                message="Welcome to the Early Dropout Prediction System. This system will help you identify students at risk.",
                type="info",
                read=False,
                created_at=now
            )
            db.add(info_notification)
            
            # Alert notification
            alert_notification = Notification(
                user_id=user.id,
                title="High Risk Students Detected",
                message="3 students have been identified as high risk. Please review them as soon as possible.",
                type="alert",
                read=False,
                created_at=now
            )
            db.add(alert_notification)
            
            # Success notification (already read)
            success_notification = Notification(
                user_id=user.id,
                title="Data Upload Complete",
                message="Student data has been successfully uploaded and processed.",
                type="success",
                read=True,
                read_at=now,
                created_at=now
            )
            db.add(success_notification)
        
        db.commit()
        print("✅ Created test notifications successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_notifications()
    print("�� Script completed") 