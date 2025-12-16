from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from app.settings import get_settings
from app.config.llm import configure_llm
from app.domains.study.controller import router as study_router

# Application Lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_llm(settings)
    yield

app = FastAPI(title="Study Chat Server", lifespan=lifespan)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.domains.subject.controller import router as subject_router
from app.domains.access.controller import router as access_router

# Include Routers
app.include_router(access_router, prefix="/api")
app.include_router(study_router, prefix="/api") 
app.include_router(subject_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8082, reload=True)
