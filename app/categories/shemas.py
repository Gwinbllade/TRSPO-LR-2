from pydantic import BaseModel


class SCategory(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SAddCategory(BaseModel):
    name: str


class SUpdateCategories(BaseModel):
    name: str
