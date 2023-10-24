import uuid

from pydantic import BaseModel, Field


class CreateStore(BaseModel):
    city: str
    email: str = Field(max_length=20)
    brand: str

    # This internal class is added to make the pydantic model compatible
    # with the ORM.
    class Config:
        orm_mode = True


class ViewStore(BaseModel):
    id: uuid.UUID = Field()
    city: str = Field()
    email: str = Field(max_length=20)
    brand: str = Field()

    class Config:
        orm_mode = True
