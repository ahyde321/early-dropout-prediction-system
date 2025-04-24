from fastapi import APIRouter, Depends, Query, HTTPException
from models.utils.system.model_info import get_model_info
from api.routes.auth import get_current_user
from db.models import User

router = APIRouter()

# 🧠 1. Get all model phases: feature importance + metrics
@router.get("/model/info", summary="Get model info for all phases")
def get_all_model_info(user: User = Depends(get_current_user)):
    return get_model_info()

# 🔍 2. Get model info for a specific phase
@router.get("/model/info/{phase}", summary="Get model info for one phase")
def get_model_info_for_phase(
    phase: str,
    user: User = Depends(get_current_user)
):
    if phase not in ["early", "mid", "final"]:
        raise HTTPException(status_code=400, detail="Invalid phase. Use early, mid, or final.")
    return get_model_info(phase)

# 📊 3. Compare performance metrics across all phases (only metrics)
@router.get("/model/metrics", summary="Compare model performance across phases")
def get_model_metrics_only(user: User = Depends(get_current_user)):
    all_info = get_model_info()
    return {phase: info.get("metrics", {}) for phase, info in all_info.items()}

# 🧬 4. Compare feature importances across all phases (only importance)
@router.get("/model/features", summary="Compare feature importance across phases")
def get_model_features_only(user: User = Depends(get_current_user)):
    all_info = get_model_info()
    return {phase: info.get("feature_importance", {}) for phase, info in all_info.items()}
