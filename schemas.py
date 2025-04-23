from pydantic import BaseModel, EmailStr


class BossSignUpSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class BossLoginSchema(BaseModel):
    email: EmailStr
    password: str


class BossNameChangeSchema(BaseModel):
    name: str


class BossPasswordChangeSchema(BaseModel):
    password: str


class BossPasswordRecoverSchema(BaseModel):
    code: str
    new_password: str

