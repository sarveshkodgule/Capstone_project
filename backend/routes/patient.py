from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from schemas.patient import PatientRiskInput
from utils.dependencies import get_current_user
from services.patient_service import assess_patient_risk, get_patient_history
import os

router = APIRouter(prefix="/patient", tags=["Patient"])

@router.post("/risk", response_model=dict)
async def calculate_patient_risk(data: PatientRiskInput, current_user: dict = Depends(get_current_user)):
    result = await assess_patient_risk(str(current_user["_id"]), data)
    return {
        "status": "success",
        "data": result,
        "message": "Risk assessment completed successfully"
    }

@router.get("/history", response_model=dict)
async def get_screening_history(current_user: dict = Depends(get_current_user)):
    """Returns all past screening submissions for the logged-in patient."""
    history = await get_patient_history(str(current_user["_id"]))
    return {
        "status": "success",
        "data": history,
        "message": f"{len(history)} screening(s) found"
    }
