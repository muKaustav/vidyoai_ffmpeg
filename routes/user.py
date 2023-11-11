from fastapi import APIRouter, Form
from core.postgres import get_all_users, create_new_user
from starlette.responses import JSONResponse

user = APIRouter()


@user.get("/")
async def get_users():
    """
    @api {get} / Get Users
    """

    try:
        response = get_all_users()  # get users from Users table

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
        response = create_new_user(name, email)  # create user in Users table

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
