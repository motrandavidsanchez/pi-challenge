from pydantic import BaseModel, Field


class CharacterLiteSchema(BaseModel):
    name: str = Field(max_length=70, min_length=3, examples=["Luke Skywalker"])
    height: int = Field(examples=[172])
    mass: int = Field(examples=[77])
    eye_color: str = Field(max_length=100, min_length=3, examples=["blue"])
    birth_year: int = Field(examples=[1998])

    class Config:
        from_attributes = True


class CharacterCreateSchema(CharacterLiteSchema):
    hair_color: str = Field(max_length=100, min_length=3, examples=["blond"])
    skin_color: str = Field(max_length=100, min_length=3, examples=["fair"])


class CharacterSchema(CharacterCreateSchema):
    id: int


class CharacterAllSchema(CharacterLiteSchema):
    id: int
