
import os
import logging
from typing import Optional
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from src.gpx_processor import process_gpx_file

# Configurações
logger = logging.getLogger(__name__)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "gpx-api",
    }

@app.post("/upload-gpx")
async def upload_gpx(
        file: UploadFile,
        user_id: str = Form(..., description="User ID"),
        max_hr: int = Form(
            210,
            ge=100,
            le=250,
            description="Maximum heart rate"
        ),
        user_weight: Optional[float] = Form(
            None,
            gt=0,
            le=300,
            description="User weight in kg"
        ),
        user_age: Optional[float] = Form(
            None,
            gt=0,
            le=120,
            description="User age"
        ),
        user_gender: Optional[str] = Form(
            None,
            description="fem or masc"
        ),
):

    logger.info(f"Recebendo upload de GPX do usuário: {user_id}")

    # I MUST separate this logic in another file!!!, for now, only testing.
    # Checks file size
    content = await file.read()

    if not file.filename.lower().endswith(".gpx"):
        raise HTTPException(
            status_code=400,
            detail="Only .gpx files are allowed"
        )

    # more validation latter?
    if file.content_type not in {
        "application/gpx+xml",
        "application/xml",
        "text/xml",
        "application/octet-stream",
    }:
        raise HTTPException(
            status_code=400,
            detail="Invalid GPX file type"
        )

    if len(content) > MAX_FILE_SIZE:
        logger.warning(f"Arquivo muito grande: {len(content)} bytes")
        raise HTTPException(status_code=413, detail="Arquivo muito grande (máximo 50MB)")

    # Processar o arquivo
    try:
        activity = process_gpx_file(
            content=content,
            user_id=user_id,
            max_hr=max_hr,
            user_weight=user_weight,
            user_age=user_age,
            user_gender=user_gender,
        )
        return activity
    except ValueError as e:
        logger.warning(f"Erro de validação: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro inesperado: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro ao processar arquivo GPX")