from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    email: str
    password: str


class CreateAdsSchema(BaseModel):
    title: str
    description: str
    user_id: int
