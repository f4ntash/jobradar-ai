from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routers import jobs

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Inicializar aplicación
app = FastAPI(
    title="Job Hunter AI API",
    description="API para gestionar ofertas laborales",
    version="0.1.0",
)

# Configurar CORS (abierto para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(jobs.router)


@app.get("/")
def root():
    """Endpoint raíz de prueba"""
    return {"message": "Job Hunter AI API running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
