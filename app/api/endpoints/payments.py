from fastapi import APIRouter, HTTPException
from app.services import stripe_service
from app.schemas import schemas

router = APIRouter()

@router.post("/create-checkout-session")
async def create_checkout_session():
    try:
        checkout_session = await stripe_service.create_checkout_session()
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session-status")
async def session_status(session_id: str):
    try:
        session = await stripe_service.get_session_status(session_id)
        return {"status": session.status, "customer_email": session.customer_details.email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))