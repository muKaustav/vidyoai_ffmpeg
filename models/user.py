from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from core.db import meta, engine


Users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("email", String(255), index=True, unique=True),
)

meta.create_all(engine)
