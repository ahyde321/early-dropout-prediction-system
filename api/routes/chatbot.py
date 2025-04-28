from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import openai
import os
from dotenv import load_dotenv
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from the correct .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

router = APIRouter()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")
logger.info(f"OpenAI API Key loaded: {'*' * 10}{openai.api_key[-4:] if openai.api_key else 'None'}")

if not openai.api_key:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ValueError("OPENAI_API_KEY environment variable is required")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    response: str

# System message to define the chatbot's behavior
SYSTEM_MESSAGE = """You are an academic advisor assistant for the Early Dropout Prediction System (EDPS).
Your role is to help advisors understand and work with the EDPS platform. You can discuss:
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

@router.post("/chat", response_model=ChatResponse)
async def chat_with_advisor(request: ChatRequest):
    try:
        logger.info(f"Received chat request with {len(request.messages)} messages")
        logger.info(f"Request content: {request.messages}")
        
        # Prepare messages with system message
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE}
        ] + [{"role": msg.role, "content": msg.content} for msg in request.messages]

        logger.info("Calling OpenAI API...")
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        logger.info("Successfully received response from OpenAI")
        return ChatResponse(response=response.choices[0].message.content)

    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        logger.error(f"OpenAI API error traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(f"Error traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
