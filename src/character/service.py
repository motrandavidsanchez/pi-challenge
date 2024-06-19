import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from src.character.models import Character
from src.character.schemas import CharacterCreateSchema


async def create_character(db: AsyncSession, data: CharacterCreateSchema) -> Character | None:
    """
    Logic to create a character in the database
    """
    try:
        result = await db.execute(insert(Character).values(**data.dict()).returning(Character))
        character = result.scalar_one_or_none()
        return character
    except IntegrityError as e:
        logging.critical(f"Error on character creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Character already exists. Check the name field"
        )


async def get_characters(db: AsyncSession) -> List[Character]:
    """
    Logic to get all characters from database
    """
    result = await db.execute(select(Character))
    characters = [row[0] for row in result.fetchall()]
    return characters


async def get_detail_character(db: AsyncSession, character_id: int) -> Character | None:
    """
    Logic to get details of a specific character by ID
    """
    result = await db.execute(select(Character).where(Character.id == character_id))
    character = result.scalar_one_or_none()
    if character is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    return character


async def delete_character(db: AsyncSession, character_id: int) -> None:
    """
    Logic to remove a character by ID
    """
    character = await get_detail_character(db=db, character_id=character_id)
    await db.delete(character)
