from typing import List
from fastapi import APIRouter
from app.schemas.compra import CompraCreate, CompraResponse
from app.models.compra_tortoise import compras

router = APIRouter(prefix="/compras", tags=["compras"])

# Crear una compra
@router.post("/", response_model=CompraResponse)
async def crear_compra(compra: CompraCreate):
    nueva_compra = await compras.create(**compra.dict())
    return CompraResponse.model_validate(nueva_compra, from_attributes=True)

# Listar compras
@router.get("/", response_model=List[CompraResponse])
async def listar_compras(skip: int = 0, limit: int = 10):
    compras_list = await compras.all().offset(skip).limit(limit)
    return [CompraResponse.model_validate(c, from_attributes=True) for c in compras_list]