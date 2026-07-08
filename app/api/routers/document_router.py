from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.schemas.document.document_upload_response import (
    DocumentUploadResponse,
)

from app.dependencies.service_dependencies import (
    get_ingestion_service,
)

from app.document.ingestion_service import IngestionService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    ingestion_service: IngestionService = Depends(
        get_ingestion_service,
    ),
):

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    destination = upload_dir / file.filename

    with open(destination, "wb") as f:
        f.write(await file.read())

    chunk_count = ingestion_service.ingest(
        str(destination),
    )

    return DocumentUploadResponse(
        success=True,
        filename=file.filename,
        chunks=chunk_count,
    )