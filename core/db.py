from decouple import config
from sqlalchemy import create_engine, MetaData

USER = config("PSQL_USER")
PASSWORD = config("PSQL_PASSWORD")
HOST = config("PSQL_HOST")
PORT = config("PSQL_PORT")
DATABASE = config("PSQL_DB")

POSTGRES_URL = (
    f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?sslmode=disable"
)

engine = create_engine(
    POSTGRES_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
)

meta = MetaData()

conn = engine.connect()
