from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, students
 
app = FastAPI(
    title="Student Roster API",
    description="Manages student roster data for AIU member districts.",
    version="1.0.0",
    docs_url="/docs",   # Swagger UI at /docs
    redoc_url="/redoc", # ReDoc at /redoc
)
 
# lets frontend call api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# including routers
app.include_router(auth.router)
app.include_router(students.router)


@app.get("/health")
def health():
    return {"status": "ok"}
