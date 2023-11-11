from fastapi import APIRouter, Form
from core.db import conn
from models.user import Users
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

user = APIRouter()


@user.get("/")
async def get_users():
    """
    @api {get} / Get Users
    """
    
    try:
        with Session(conn) as session:
            result = session.execute(Users.select()).fetchall()
            result_list = []

            for row in result:
                try:
                    result_list.append(
                        {
                            "name": row[1],
                            "email": row[2],
                        }
                    )

                except Exception as e:
                    print(str(e))

            response = {"status": "successful", "data": result_list}

            return JSONResponse(
                content=response,
                media_type="application/json",
                status_code=200,
            )

    except Exception as e:
        response = {
            "status": "failed",
            "message": str(e),
        }

        return JSONResponse(
            content=response,
            media_type="application/json",
            status_code=500,
        )


@user.post("/")
async def create_user(name: str = Form(...), email: str = Form(...)):
    """
    @api {post} / Create User
    @formData {String} name Name of the user
    @formData {String} email Email of the user
    """

    try:
        with Session(conn) as session:
            new_user = {"name": name, "email": email}

            session.execute(Users.insert().values(new_user))
            session.commit()

            response = {"status": "successful", "message": "User created successfully."}

            return JSONResponse(
                content=response,
                media_type="application/json",
                status_code=200,
            )

    except Exception as e:
        response = {
            "status": "failed",
            "message": str(e),
        }

        return JSONResponse(
            content=response,
            media_type="application/json",
            status_code=500,
        )
