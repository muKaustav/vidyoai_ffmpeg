from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    User Schema
    """

    name: str
    email: str
