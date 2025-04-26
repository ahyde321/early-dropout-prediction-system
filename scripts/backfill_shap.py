# scripts/backfill_shap_values.py

import os
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import RiskPrediction, Student
from models.utils.system.shap_explainer import explain_student

def backfill_missing_shap_values():
    db: Session = SessionLocal()

    try:
        predictions = db.query(RiskPrediction).filter(RiskPrediction.shap_values.is_(None)).all()
        print(f"🧠 Found {len(predictions)} predictions missing SHAP values.")

        updated = 0

        for pred in predictions:
            student = db.query(Student).filter(Student.student_number == pred.student_number).first()
            if not student:
                print(f"⚠️ Skipping missing student {pred.student_number}")
                continue

            student_dict = student.__dict__.copy()
            student_dict.pop("_sa_instance_state", None)

            try:
                shap_values = explain_student(student_dict)
                pred.shap_values = shap_values
                updated += 1
                print(f"✅ Backfilled SHAP for {pred.student_number} / phase {pred.model_phase}")
            except Exception as e:
                print(f"❌ Failed to generate SHAP for {pred.student_number}: {e}")

        db.commit()
        print(f"✅ Done. {updated} predictions updated with SHAP values.")

    finally:
        db.close()

if __name__ == "__main__":
    backfill_missing_shap_values()
