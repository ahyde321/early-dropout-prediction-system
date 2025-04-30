from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from db.database import get_db
from db.models import Notification, User, Student
from api.schemas import (
    NotificationResponse, 
    NotificationCreate, 
    NotificationUpdate,
    NotificationPreferences
)
from api.routes.auth import get_current_user

router = APIRouter(tags=["Notifications"])


@router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False
):
    print(f"🔔 Fetching notifications for user_id={current_user.id}, unread_only={unread_only}")
    """Get all notifications for the current user with optional filtering"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    if unread_only:
        query = query.filter(Notification.read == False)
    return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/notifications/count", response_model=dict)
async def get_notification_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get count of unread notifications for the current user"""
    unread_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.read == False
    ).count()
    return {"unread_count": unread_count}


@router.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific notification"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.post("/notifications", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new notification (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can create notifications")

    target_user = db.query(User).filter(User.id == notification_data.user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    if notification_data.student_number:
        student = db.query(Student).filter(Student.student_number == notification_data.student_number).first()
        if not student:
            raise HTTPException(status_code=404, detail="Referenced student not found")

    notification = Notification(
        user_id=notification_data.user_id,
        title=notification_data.title,
        message=notification_data.message,
        type=notification_data.type,
        student_number=notification_data.student_number,
        read=False,
        created_at=datetime.utcnow()
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


@router.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a specific notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.read = True
    notification.read_at = datetime.utcnow()

    db.commit()
    db.refresh(notification)
    return notification


@router.patch("/notifications/read-all", response_model=dict)
async def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read for the current user"""
    updated = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.read == False
    ).update({
        Notification.read: True,
        Notification.read_at: datetime.utcnow()
    })
    db.commit()
    return {"message": f"Marked {updated} notifications as read"}


@router.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a notification (admin or notification owner only)"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    if notification.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You don't have permission to delete this notification")

    db.delete(notification)
    db.commit()
    return None


@router.delete("/notifications/clear", response_model=dict)
async def clear_all_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete all notifications for the current user"""
    deleted = db.query(Notification).filter(Notification.user_id == current_user.id).delete()
    db.commit()
    return {"message": f"Deleted {deleted} notifications"}


@router.post("/notifications/broadcast", response_model=dict)
async def broadcast_notification(
    title: str,
    message: str,
    type: str = "info",
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a notification to multiple users based on role (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can broadcast notifications")

    query = db.query(User).filter(User.is_active == True)
    if role:
        query = query.filter(User.role == role)

    users = query.all()
    notifications = []
    for user in users:
        notification = Notification(
            user_id=user.id,
            title=title,
            message=message,
            type=type,
            read=False,
            created_at=datetime.utcnow()
        )
        db.add(notification)
        notifications.append(notification)

    db.commit()
    return {"message": f"Sent notification to {len(notifications)} users"}


@router.post("/notifications/for-student/{student_number}", response_model=dict)
async def create_notification_for_student_advisors(
    student_number: str,
    title: str,
    message: str,
    type: str = "alert",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a notification about a student for all advisors (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can broadcast notifications")

    student = db.query(Student).filter(Student.student_number == student_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    advisors = db.query(User).filter(
        User.role == "advisor",
        User.is_active == True
    ).all()

    for advisor in advisors:
        notification = Notification(
            user_id=advisor.id,
            title=title,
            message=message,
            type=type,
            student_number=student_number,
            read=False,
            created_at=datetime.utcnow()
        )
        db.add(notification)

    db.commit()
    return {"message": f"Sent notification about student {student_number} to {len(advisors)} advisors"}
