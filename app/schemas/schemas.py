from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


########################################################################################################################################    
class ClientRequest(BaseModel):
    client_name: str = Field(..., max_length=100, description="Nombre del cliente.")
    birth_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Fecha de nacimiento en formato AAAA-MM-DD.")
    client_email: Optional[str] = Field(None, max_length=120, description="Email del cliente (opcional).")
    creature_details: str = Field(..., max_length=2000, description="Detalles de la criatura mágica que se desea generar.")

class CreatureBase(BaseModel):
    name: str = Field(..., max_length=50, description="Nombre de la criatura.")
    description: str = Field(..., max_length=5000, description="Descripción mágica de la criatura.")
    unique_number: int = Field(..., description="Número único asociado con la criatura.")
    image_url: str = Field(..., max_length=500, description="URL o nombre de archivo de la imagen generada.")

class CreatureResponse(CreatureBase):
    QR_code_url: Optional[str] = Field(None, max_length=500, description="URL del código QR relacionado con la criatura (opcional).")
    id: Optional[int] = Field(None, description="Identificador único de la criatura.")
    owner_id: Optional[int] = Field(None, description="Identificador del dueño de la criatura.")
    created_at: Optional[datetime] = Field(None, description="Fecha y hora de creación de la criatura.")
    class Config:
        from_attributes = True

class PurchaseRequest(BaseModel):
    client_name: str
    client_email: str
    birth_date: str
    creature_name: str
    creature_description: str
    wheel_number: int
    image_url: str

class PurchaseResponse(CreatureResponse):
    pass
########################################################################################################################################

class CreatureCreate(CreatureBase):
    owner_id: int
    class Config:
        from_attributes = True



class ClientBase(BaseModel):
    name: str = Field(..., max_length=50)
    email: str = Field(..., max_length=120)
    birthdate: Optional[date]

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class WheelBase(BaseModel):
    numero: int

class WheelCreate(WheelBase):
    pass

class WheelResponse(WheelBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True





# Nuevos esquemas para Book y Scene

class BookBase(BaseModel):
    title: str
    client_id: int
    scene_count: int = 20
    completion_status: bool = False
    is_paid: bool = False

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SceneBase(BaseModel):
    book_id: int
    paragraph: Optional[str]
    image_url: Optional[str]
    scene_number: int

class SceneCreate(SceneBase):
    pass

class SceneResponse(SceneBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

