from fastapi import FastAPI
from app.api.routes import auth, health, tasks
from app.api.routes import users

app = FastAPI(
    title="Task Manager API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Register routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Task Manager API is up and running"}
