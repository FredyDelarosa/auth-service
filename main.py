from fastapi import FastAPI
from core.db.connection import engine, Base
from features.auth.infrastructure.routers import router as auth_router

# Crear tablas en BD al inicio (en prod usar Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PyroGuard Auth Service",
    docs_url="/auth/docs",
    openapi_url="/auth/openapi.json",
    redoc_url="/auth/redoc"
)

app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
