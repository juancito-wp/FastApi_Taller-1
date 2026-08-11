from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class TraineeBase(BaseModel):
    tipo_doc: str = Field(..., description="Tipo de documento del aprendiz (CC, TI, CE)", pattern =r"^(CC|TI|CE)$", example="CC")
    documento: str = Field(..., description="Número de documento del aprendiz", min_length=5, max_length=10, example="123456789", pattern="^[0-9]+$" )
    nombre: str = Field(..., description="Nombre completo del aprendiz", min_length=3, max_length=50, example="Juan Perez", pattern="^[A-Za-z ]+$")
    ficha: str = Field(..., description="Número de ficha del aprendiz", min_length=5, max_length=10, example="2023-001", pattern="^[0-9]+$")
    programa: str = Field(..., description="Nombre del programa de formación del aprendiz", min_length=3, max_length=50, example="Programación", pattern="^[A-Za-z ]+$")
    email: EmailStr = Field(..., description="Correo electrónico del aprendiz", example="juan.perez@example.com")


class TraineeCreate(TraineeBase):
    pass


class TraineeUpdate(BaseModel):
    tipo_doc: Optional[str] = Field(None, pattern=r"^(CC|TI|CE)$",)
    nombre: Optional[str] = Field(None, min_length=3)
    ficha: Optional[str] = Field(None, pattern="^[0-9]+$")
    programa: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = Field(None)


class TraineeResponse(TraineeBase):
    data: Optional[List[TraineeBase]] = None # Datos cosumidos de la API rick y morty