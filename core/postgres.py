from decouple import config
from core.db import conn
from sqlalchemy.orm import Session
from models.task import AudioExtractTasks, WatermarkTasks


def get_audio_task(unique_id):
    try:
        with Session(bind=conn) as db:
            result = db.execute(
                AudioExtractTasks.select().where(
                    AudioExtractTasks.c.timestamp == unique_id
                )
            ).fetchone()

            if result is None:
                response = {
                    "status": "failed",
                    "message": "task not found",
                }

                return response

            else:
                response = {
                    "status": "success",
                    "data": {
                        "email": result[1],
                        "status": result[2],
                        "url": result[3],
                    },
                }

                return response

    except Exception as e:
        raise Exception(str(e))

    finally:
        db.close()


def add_audio_task(email, timestamp):
    try:
        with Session(bind=conn) as db:
            new_task = {"email": email, "status": "pending", "timestamp": timestamp}

            db.execute(
                AudioExtractTasks.insert().values(new_task)
            )  # insert task to db with status "pending"
            db.commit()

    except Exception as e:
        raise Exception(str(e))

    finally:
        db.close()


def update_audio_task(audio_file_path, email, timestamp):
    audio_file_url = f"https://{config('S3_BUCKET_NAME')}.s3.amazonaws.com/{audio_file_path.split('/')[-1]}"

    update_task = {"status": "completed", "url": audio_file_url}

    try:
        with Session(bind=conn) as db:
            db.execute(
                AudioExtractTasks.update()
                .where(
                    (AudioExtractTasks.c.email == email)
                    & (AudioExtractTasks.c.timestamp == timestamp)
                )
                .values(update_task)
            )

            db.commit()

    except Exception as e:
        raise Exception(str(e))

    finally:
        db.close()


def get_video_task(unique_id):
    try:
        with Session(bind=conn) as db:
            result = db.execute(
                WatermarkTasks.select().where(WatermarkTasks.c.timestamp == unique_id)
            ).fetchone()

            if result is None:
                response = {
                    "status": "failed",
                    "message": "task not found",
                }

                return response

            else:
                response = {
                    "status": "success",
                    "data": {
                        "email": result[1],
                        "status": result[3],
                        "url": result[4],
                    },
                }

                return response

    except Exception as e:
        raise Exception(str(e))

    finally:
        db.close()


def add_video_watermark_task(email, timestamp, watermark_params):
    try:
        with Session(bind=conn) as db:
            new_task = {
                "email": email,
                "status": "pending",
                "timestamp": timestamp,
                "watermark_params": watermark_params,
            }

            db.execute(
                WatermarkTasks.insert().values(new_task)
            )  # insert task to db with status "pending"
            db.commit()

    except Exception as e:
        raise Exception(str(e))

    finally:
        db.close()


def update_video_task(video_file_path, email, timestamp):
    video_file_url = f"https://{config('S3_BUCKET_NAME')}.s3.amazonaws.com/{video_file_path.split('/')[-1]}"

    update_task = {"status": "completed", "url": video_file_url}

    try:
        with Session(bind=conn) as db:
            db.execute(
                WatermarkTasks.update()
                .where(
                    (WatermarkTasks.c.email == email)
                    & (WatermarkTasks.c.timestamp == timestamp)
                )
                .values(update_task)
            )

            db.commit()

    except Exception as e:
        raise Exception(str(e))

    finally:
        db.close()
