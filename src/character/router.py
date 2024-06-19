from typing import List

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.character.schemas import CharacterSchema, CharacterLiteSchema, CharacterCreateSchema, CharacterAllSchema
from src.settings.database import get_db_session
from src.character import service


router = APIRouter()


@router.post(
    path="/add",
    status_code=status.HTTP_201_CREATED,
    response_model=CharacterSchema,
    tags=["Character"],
    summary="Create Character in the app"
)
async def create(data: CharacterCreateSchema, db: AsyncSession = Depends(get_db_session)):
    character = await service.create_character(db=db, data=data)
    return character


@router.get(
    path="/getAll",
    status_code=status.HTTP_200_OK,
    response_model=List[CharacterAllSchema],
    tags=["Character"],
    summary="Get all the Characters in the app"
)
async def get_all(db: AsyncSession = Depends(get_db_session)):
    characters = await service.get_characters(db=db)
    return characters


@router.get(
    path="/get/{character_id}",
    status_code=status.HTTP_200_OK,
    response_model=CharacterSchema,
    tags=["Character"],
    summary="Get details of a specific Character by app ID"
)
async def detail(character_id: int = Path(..., gt=0, example=1), db: AsyncSession = Depends(get_db_session)):
    character = await service.get_detail_character(db=db, character_id=character_id)
    return character


@router.delete(
    path="/delete/{character_id}",
    status_code=status.HTTP_200_OK,
    tags=["Character"],
    summary="Delete a character by app ID"
)
async def delete(character_id: int = Path(..., gt=0, example=1), db: AsyncSession = Depends(get_db_session)):
    await service.delete_character(db=db, character_id=character_id)
    return {"detail": "The character has been deleted"}
