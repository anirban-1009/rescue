from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.first_responder import router as FirstResponderRouter

app = FastAPI(
    title="Rescue API",
    description="API for First Responder Management System",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    FirstResponderRouter, tags=["First Responders"], prefix="/v1/firstResponder"
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Rescue API"}
