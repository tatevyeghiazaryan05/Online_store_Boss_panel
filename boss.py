from fastapi import APIRouter, Depends, HTTPException, status
import main
from schemas import BossNameChangeSchema, BossPasswordChangeSchema, BossPasswordRecoverSchema
from security import get_current_boss, pwd_context
from pydantic import EmailStr
from email_service import send_verification_email
from datetime import datetime, timedelta


boss_router = APIRouter()


@boss_router.put("/api/boss/change/name")
def change_boss_name(data: BossNameChangeSchema, token=Depends(get_current_boss)):
    boss_id = token["id"]
    main.cursor.execute("UPDATE boss SET name = %s WHERE id = %s", (data.name, boss_id))
    main.conn.commit()
    return "Updated successfully!!"


@boss_router.put("/api/boss/change/password")
def change_boss_password(data: BossPasswordChangeSchema, token=Depends(get_current_boss)):
    boss_id = token["id"]
    new_hashed_password = pwd_context.hash(data.password)
    main.cursor.execute("UPDATE boss SET password = %s WHERE id = %s",
                        (new_hashed_password, boss_id))
    main.conn.commit()
    return "Password updated successfully!!"


@boss_router.get("/api/boss/my-account-info")
def get_boss_my_account_info(token=Depends(get_current_boss)):
    boss_id = token["id"]
    main.cursor.execute("SELECT email,name FROM boss WHERE id=%s",
                        (boss_id,))
    data = main.cursor.fetchall()
    return data


@boss_router.get("/api/boss/for/forgot/password/code/{email}")
def boss_forgot_password_code(email: EmailStr):
    try:
        main.cursor.execute("SELECT * FROM boss WHERE email=%s",
                            (email,))
        boss = main.cursor.fetchone()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error"
        )

    if not boss:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not such boss!"

        )
    verification_code = send_verification_email(email)
    main.cursor.execute("INSERT INTO forgotpasswordcode (code,email) VALUES(%s,%s)",
                        (verification_code, email))

    main.conn.commit()


@boss_router.post("/api/boss/forgot/password")
def boss_forgot_password(data: BossPasswordRecoverSchema):
    code = data.code

    new_password = pwd_context.hash(data.new_password)

    try:
        main.cursor.execute("SELECT * FROM forgotpasswordcode WHERE code=%s",
                        (code,))
        data = main.cursor.fetchone()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error"
        )

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code is incorrect!"

        )

    data = dict(data)
    created_at = data.get("created_at")
    expiration_time = created_at + timedelta(minutes=15)
    if datetime.now() > expiration_time:
        main.cursor.execute("DELETE FROM forgotpasswordcode WHERE code=%s", (code,))
        main.conn.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code has expired after 15 minutes."
        )

    main.cursor.execute("UPDATE boss SET password =%s WHERE email=%s",
                        (new_password, data["email"]))

    main.conn.commit()

    main.cursor.execute("DELETE FROM forgotpasswordcode WHERE code = %s",
                        (code,))
    main.conn.commit()
    return "Changed password successfully!!"


@boss_router.put("/api/boss/boss/password/recovery")
def password_recovery(data: BossPasswordChangeSchema, token=Depends(get_current_boss)):
    boss_id = token["id"]
    new_password = pwd_context.hash(data.password)
    main.cursor.execute("UPDATE boss SET password =%s WHERE id=%s",
                        (new_password, boss_id))
    main.conn.commit()
    return "New password updated successfully!!"
