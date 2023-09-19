from pydantic import BaseModel, Field


class CreateStore(BaseModel):
    city: str
    email: str = Field(max_length=20)
    brand: str


class ViewStore(BaseModel):
    id: int = Field()
    city: str = Field()
    email: str = Field(max_length=20)
    brand: str = Field()
