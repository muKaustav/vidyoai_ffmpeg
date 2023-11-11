import os
import time
from fastapi import APIRouter, File, UploadFile, Form, Path
from core.postgres import add_audio_task, get_audio_task
from worker.tasks import process_audio
from starlette.responses import JSONResponse

audio = APIRouter()


def get_current_epoch():
    return str(int(time.time()))


@audio.post("/extract")
async def audio_extract(file: UploadFile = File(...), email: str = Form(...)):
    """
    @api {post} /audio-extract Create Audio Extract Task
    @formData {String} email Email of the user
    @formData {File} file File to be uploaded
    """

    CURRENT_EPOCH = get_current_epoch()

    try:
        add_audio_task(email, CURRENT_EPOCH)  # add audio task to db

        file_name = file.filename
        file_extension = file_name.split(".")[-1]

        file_path = os.path.join("worker/media", f"{CURRENT_EPOCH}.{file_extension}")

        with open(file_path, "wb+") as file_object:  # save file to disk
            file_object.write(file.file.read())

        process_audio.delay(file_path, email, CURRENT_EPOCH)  # process audio

        response = {
            "status": "success",
            "message": "audio extraction task has been created",
            "unique_id": CURRENT_EPOCH,
        }

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


@audio.get("/extract/{unique_id}")
async def audio_extract(unique_id: str = Path(...)):
    """
    @api {get} /audio-extract/:unique_id Get Audio Extract Task
    @pathParam {String} unique_id Unique ID of the task
    """

    try:
        response = get_audio_task(unique_id)  # get audio task with unique_id

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
