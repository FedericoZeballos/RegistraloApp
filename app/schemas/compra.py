from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base común
class CompraBase(BaseModel):
    nombre: Optional[str] = None
    descripcion: str
    categoria: Optional[str] = None
    monto: float

# Esquema para crear una nueva compra
class CompraCreate(CompraBase):
    pass  # hereda todo

# Esquema para devolver datos al cliente
class CompraResponse(CompraBase):
    id: int
    fecha: datetime

    model_config = {
        "from_attributes": True
    }