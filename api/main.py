import os
import time
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from db.database import engine
from db.models import Base

# === Routers ===
from api.routes import (
    students,
    prediction,
    uploads,
    admin,
    auth,
    summary,
    model
)

# === Load .env and Set Environment ===
load_dotenv()
ENV = os.getenv("ENV", "production")
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8080')
print("🌱 Loaded FRONTEND_URL from .env:", FRONTEND_URL)

# === FastAPI App ===
app = FastAPI(title="Early Dropout Prediction System", version="1.0")

# === CORS Middleware ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# === Logging Middleware ===
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    formatted_duration = f"{duration:.2f}s"
    print(f"{request.method} {request.url.path} → {response.status_code} [{formatted_duration}]")
    return response

# === Rate Limiting ===
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# === Database Init ===
Base.metadata.create_all(bind=engine)

# === API Routers ===
app.include_router(students.router, prefix="/api", tags=["Students"])
app.include_router(prediction.router, prefix="/api", tags=["Predictions"])
app.include_router(uploads.router, prefix="/api", tags=["Uploads"])
app.include_router(admin.router, prefix="/api", tags=["Admin"])
app.include_router(summary.router, prefix="/api", tags=["Summary"])
app.include_router(model.router, prefix="/api", tags=["Model"])


# Optional: Enable auth
app.include_router(auth.router, prefix="/api", tags=["Auth"])

# === Environment Info ===
print(f"🚀 Environment: {ENV}")
print(f"🌐 Allowed Frontend Origin: {FRONTEND_URL}")

# === Health Check Endpoint ===
@app.get("/", tags=["Health"])
@limiter.limit("10/minute")
def root(request: Request):
    return {"message": "EDPS is live!"}


from db.database import engine
from db.models import Base
