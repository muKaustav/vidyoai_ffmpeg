from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from core.db import meta, engine

"""
Audio Extract Tasks Table
"""
AudioExtractTasks = Table(
    "audio_extract_tasks",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(255)),
    Column("status", String(255), default="pending"),
    Column("url", String(255), nullable=True),
    Column("timestamp", String(255)),
)


"""
Video Watermark Tasks Table
"""
WatermarkTasks = Table(
    "watermark_tasks",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(255)),
    Column("watermark_params", String, nullable=True),
    Column("status", String(255), default="pending"),
    Column("url", String(255), nullable=True),
    Column("timestamp", String(255)),
)

meta.create_all(engine)
