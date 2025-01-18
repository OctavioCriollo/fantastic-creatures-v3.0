from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.services import openai_service, utils_service
from app.services.dalle_service import AI_image_creature_generator # Update: Import changed
from app.config import settings
import os
from fastapi.responses import FileResponse
from pydantic import ValidationError

router = APIRouter()

@router.get("/")
async def home():
    return {"message": "¡Bienvenido a tu proyecto FastAPI!"}

@router.get("/static/qr_codes/{filename}")
async def serve_qr_code(filename: str):
    qr_file_path = os.path.join(os.getcwd(), 'static', 'qr_codes')
    file_path = os.path.join(qr_file_path, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="QR code not found")
    return FileResponse(file_path)

@router.get("/static/creatures/{filename}")
async def serve_creature_image(filename: str):
    creatures_file_path = os.path.join(os.getcwd(), 'static', 'creatures')
    file_path = os.path.join(creatures_file_path, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Creature image not found")
    return FileResponse(file_path)

@router.post("/generate_creature", response_model=schemas.CreatureResponse)
async def generate_creature(
    #client_request: schemas.ClientRequest,
    client_request: dict = Body(...),  # Recibe la solicitud como un diccionario sin validación automática
    db: Session = Depends(get_db)
):
    # Validación manual de los campos
    if "client_name" not in client_request or not client_request["client_name"]:
        raise HTTPException(status_code=400, detail="Se requiere el nombre del cliente.")
    if "birth_date" not in client_request or not client_request["birth_date"]:
        raise HTTPException(status_code=400, detail="Se requiere la fecha de nacimiento.")
    if "creature_details" not in client_request or not client_request["creature_details"]:
        raise HTTPException(status_code=400, detail="Se requieren los detalles de la criatura.")

    try:
        # Verificar que hay números disponibles en la ruleta
        wheel_count = db.query(models.Wheel).count()
        if wheel_count == 0:
            raise HTTPException(status_code=400, detail="No hay números disponibles en la ruleta.")

        try:
            # Llamar al servicio para generar la descripción de la criatura
            creature = await openai_service.AI_description_creature_generator(
                client_request["client_name"],
                client_request["birth_date"],
                client_request["creature_details"]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while generating the creature description: {str(e)}")

        return schemas.CreatureResponse(**creature)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar la criatura: {str(e)}")






@router.post("/buy_creature", response_model=schemas.CreatureResponse)
async def buy_creature(
    purchase_request: schemas.PurchaseRequest,
    db: Session = Depends(get_db)
):
    wheel_entry = db.query(models.Wheel).filter_by(numero=purchase_request.wheel_number).first()
    if not wheel_entry:
        raise HTTPException(status_code=404, detail="Ya ha sido comprada esta imagen")

    client = db.query(models.Client).filter_by(name=purchase_request.client_name, email=purchase_request.client_email).first()
    if not client:
        client = models.Client(name=purchase_request.client_name, email=purchase_request.client_email, birthdate=purchase_request.birth_date)
        db.add(client)
        db.commit()
        db.refresh(client)

    creature = models.Creature(
        name=purchase_request.creature_name,
        description=purchase_request.creature_description,
        unique_number=purchase_request.wheel_number,
        owner_id=client.id,
        image_url=purchase_request.image_url
    )

    db.add(creature)
    db.flush()

    qr_code_url = await utils_service.generate_qr_code(creature, purchase_request.client_name, purchase_request.birth_date)
    if "Error:" in qr_code_url:
        raise HTTPException(status_code=400, detail=qr_code_url)

    creature.QR_code_url = qr_code_url

    db.delete(wheel_entry)
    db.commit()
    db.refresh(creature)

    return schemas.CreatureResponse.from_orm(creature)

