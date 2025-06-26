from fastapi import FastAPI
from app.api.routes import auth, health, tasks
from app.api.routes import users
from prometheus_fastapi_instrumentator import Instrumentator
from app.config import settings

app = FastAPI(
    title="Task Manager API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
Instrumentator().instrument(app).expose(app)

# Register routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Task Manager API is up and running"}
