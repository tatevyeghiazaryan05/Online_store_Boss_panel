from pydantic import BaseModel, EmailStr


class BossSignUpSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class BossLoginSchema(BaseModel):
    email: EmailStr
    password: str
