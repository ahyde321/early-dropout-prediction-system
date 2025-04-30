from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import logging
import traceback
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Student, RiskPrediction

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ValueError("OPENAI_API_KEY environment variable is required")

client = OpenAI(api_key=api_key)
logger.info(f"OpenAI API Key loaded: {'*' * 10}{api_key[-4:]}")

# FastAPI router
router = APIRouter()

# Request/Response schemas
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    student_number: Optional[str] = None
    alerts: Optional[bool] = True

class ChatResponse(BaseModel):
    response: str

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# System message for assistant behavior
SYSTEM_MESSAGE = """You are an academic advisor assistant for the Early Dropout Prediction System (EDPS).
Your role is to help advisors understand and work with the EDPS platform. Keep your responses concise, practical, and no more than 4 bullet points or 100 words.
Avoid long paragraphs. Prioritise clarity and relevance. You can discuss:
- Student dropout risk factors and predictions
- How risk scores are calculated
- Recommended intervention strategies
- Where to find student data in the system
- Early warning signs to monitor

You must:
- Stay focused on EDPS-related topics
- Provide accurate, professional advice
- Maintain confidentiality
- Refuse to answer questions outside your scope

If asked about topics outside EDPS, politely decline and redirect to EDPS-related matters."""

def get_student_context(student_number: str, db: Session) -> Optional[str]:
    student = db.query(Student).filter(Student.student_number == student_number).first()
    prediction = (
        db.query(RiskPrediction)
        .filter(RiskPrediction.student_number == student_number)
        .order_by(RiskPrediction.timestamp.desc())
        .first()
    )
    if not student:
        return None

    context = f"Student {student.first_name} {student.last_name} ({student.student_number})"

    if prediction:
        context += (
            f" is predicted to be {prediction.risk_level.upper()} risk "
            f"with a score of {prediction.risk_score:.2f} "
            f"({prediction.model_phase} phase, updated on {prediction.timestamp.date()})."
        )

    # Add more context fields here
    context += f"\n\nAcademic data:\n"
    context += f"- 1st Sem Approved Units: {student.curricular_units_1st_sem_approved}\n"
    context += f"- 1st Sem Grade: {student.curricular_units_1st_sem_grade}\n"
    context += f"- 2nd Sem Grade: {student.curricular_units_2nd_sem_grade}\n"
    context += f"- Age at enrollment: {student.age_at_enrollment}\n"
    context += f"- Displaced: {student.displaced}\n"
    context += f"- Tuition up to date: {student.tuition_fees_up_to_date}\n"
    context += f"- Gender: {student.gender}\n"
    context += f"- Scholarship holder: {student.scholarship_holder}\n"

    return context

# Chat endpoint
@router.post("/chat", response_model=ChatResponse)
async def chat_with_advisor(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received chat request with {len(request.messages)} messages")

        messages = [{"role": "system", "content": SYSTEM_MESSAGE}]

        # Add student-specific context if student number provided
        if request.student_number:
            context = get_student_context(request.student_number, db)
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Student context: {context}"
                })

        # Add user-assistant conversation history
        messages += [{"role": msg.role, "content": msg.content} for msg in request.messages]

        logger.info("Calling OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        logger.info("Response received successfully.")
        return ChatResponse(response=reply)

    except OpenAIError as e:
        logger.error("OpenAI API error", exc_info=True)
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        logger.error("Internal server error", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
