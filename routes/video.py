import os
import time
from fastapi import APIRouter, UploadFile, Form, Path, Query
from core.postgres import add_video_watermark_task, get_video_task
from worker.tasks import process_video_watermark
from starlette.responses import JSONResponse
from typing import List

video = APIRouter()


def get_current_epoch():
    """
    Get current epoch time
    """
    return str(int(time.time()))


@video.post("/watermark")
async def video_watermark(
    files: List[UploadFile],
    email: str = Form(...),
    x_offset: int = Query(0),
    y_offset: int = Query(0),
):
    """
    @api {post} /video-watermark Create Video Watermark Task
    @formData {List[UploadFile]} files List of files to upload
    @formData {String} email Email of the user
    @queryParam {Number} x_offset X offset of the watermark, default: 0
    @queryParam {Number} y_offset Y offset of the watermark, default: 0
    """

    CURRENT_EPOCH = get_current_epoch()

    try:
        file = files[0]
        watermark = files[1]

        watermark_params = f"scale=200:200,overlay=W-w{x_offset}:H-h{y_offset}"
        add_video_watermark_task(
            email, CURRENT_EPOCH, watermark_params
        )  # add video watermark task to db

        file_name = file.filename
        file_extension = file_name.split(".")[-1]

        watermark_name = watermark.filename
        watermark_extension = watermark_name.split(".")[-1]

        file_path = os.path.join("worker/media", f"{CURRENT_EPOCH}.{file_extension}")
        watermark_path = os.path.join(
            "worker/media", f"{CURRENT_EPOCH}_watermark.{watermark_extension}"
        )

        with open(file_path, "wb+") as file_object:
            file_object.write(file.file.read())

        with open(watermark_path, "wb+") as watermark_object:
            watermark_object.write(watermark.file.read())

        # Process video watermark
        process_video_watermark.delay(
            file_path, watermark_path, x_offset, y_offset, email, CURRENT_EPOCH
        )

        response = {
            "status": "success",
            "message": "video watermarking task has been created",
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


@video.get("/watermark/{unique_id}")
async def watermark(unique_id: str = Path(...)):
    """
    @api {get} /video-watermark/:unique_id Get Video Watermark Task
    @pathParam {String} unique_id Unique ID of the task
    """

    try:
        response = get_video_task(unique_id)  # get video task with unique_id

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
