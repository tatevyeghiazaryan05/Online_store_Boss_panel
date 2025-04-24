import main
from fastapi import APIRouter, HTTPException, status, Form, UploadFile, File
from schemas import BossSignUpSchema, BossLoginSchema
from security import pwd_context, create_access_token


authrouter = APIRouter()


@authrouter.post("/api/boss/auth/sign-up")
def user_signup(sign_up_data: BossSignUpSchema):
    name = sign_up_data.name
    email = sign_up_data.email
    password = sign_up_data.password

    hashed_password = pwd_context.hash(password)

    main.cursor.execute("""INSERT INTO boss (name, email, password) VALUES(%s,%s,%s)""",
                        (name, email, hashed_password))
    main.conn.commit()

    return "Sign Up Successfully!!"


@authrouter.post("/api/boss/auth/login")
def user_login(login_data: BossLoginSchema):
    email = login_data.email
    password = login_data.password

    main.cursor.execute("""SELECT * FROM boss WHERE  email = %s""",
                        (email,))

    boss = main.cursor.fetchone()
    boss = dict(boss)
    boss_password_db = boss.get("password")

    if not pwd_context.verify(password, boss_password_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="password is not correct!!"
        )

    else:
        boss_id_db = boss.get("id")
        boss_email_db = boss.get("email")

        return create_access_token({"id": boss_id_db,
                                    "email": boss_email_db})

