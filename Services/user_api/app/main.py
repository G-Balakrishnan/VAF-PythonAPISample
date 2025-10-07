from fastapi import FastAPI
from unnoti_dbforge.migration_runner import run_migrations
from app.api.user_routes import router as user_router

app = FastAPI(
    title="Unnoti User API",
    description="User management microservice with CRUD operations",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup():
    run_migrations()

app.include_router(user_router, prefix="/users")