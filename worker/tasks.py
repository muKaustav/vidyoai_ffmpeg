from __future__ import absolute_import, unicode_literals
import os
from celery import shared_task
from celery.utils.log import get_task_logger
from core.s3 import create_presigned_post
from core.postgres import update_audio_task, update_video_task
import subprocess

logger = get_task_logger(__name__)


@shared_task(bind=True, name="remove_temp_files")
def remove_temp_files(self, video_path, audio_path, watermark_video_path=None):
    """
    Remove temp files
    """

    try:
        os.remove(video_path)  # remove video file
        os.remove(audio_path)  # remove audio file

        if watermark_video_path is not None:
            os.remove(watermark_video_path)  # remove watermark video file

    except Exception as e:
        logger.error(str(e))
        raise Exception(str(e))

    finally:
        return True


@shared_task(bind=True, name="process_audio_util")
def process_audio_util(self, video_file_path, audio_file_path, email, timestamp):
    """
    Extract audio from video
    """

    try:
        commands = [
            "ffmpeg",
            "-i",
            video_file_path,
            audio_file_path,
        ]

        subprocess.run(commands)  # Example: ffmpeg -i video.mp4 audio.mp3

        create_presigned_post(audio_file_path)  # upload to s3

        update_audio_task(
            audio_file_path, email, timestamp
        )  # update db status to "completed"

        remove_temp_files.delay(video_file_path, audio_file_path)  # remove temp files

    except Exception as e:
        logger.error(str(e))
        raise Exception(str(e))

    finally:
        return True


@shared_task(bind=True, name="process_audio")
def process_audio(self, file_path, email, timestamp):
    """
    Process audio
    """

    logger.info("Starting audio processing...")

    try:
        file_ext = file_path.split(".")[-1]

        audio_file_path = (
            f"worker/media/{file_path.split('/')[-1].replace(file_ext, 'mp3')}"
        )

        process_audio_util.delay(
            file_path, audio_file_path, email, timestamp
        )  # extract audio

    except Exception as e:
        logger.error(str(e))
        raise Exception(str(e))

    finally:
        logger.info("Finished audio processing...")
        return True


@shared_task(bind=True, name="process_video_util")
def process_video_util(
    self,
    video_file_path,
    watermark_file_path,
    x_offset,
    y_offset,
    email,
    timestamp,
):
    """
    Add watermark to video
    """

    try:
        output_video_path = f"worker/media/proc_{video_file_path.split('/')[-1]}"

        commands = [
            "ffmpeg",
            "-i",
            video_file_path,
            "-i",
            watermark_file_path,
            "-filter_complex",
            f"[1]scale=min(iw\,100):min(ih\,100) [watermark]; [0][watermark]overlay=W-w-{x_offset}:H-h-{y_offset}",
            output_video_path,
        ]

        subprocess.run(
            commands
        )  # Example: ffmpeg -i video.mp4 -i watermark.png -filter_complex "[1]scale=min(iw\,100):min(ih\,100) [watermark]; [0][watermark]overlay=W-w-10:H-h-10" output.mp4

        create_presigned_post(output_video_path)  # Upload to S3

        update_video_task(
            output_video_path, email, timestamp
        )  # Update db status to "completed"

        remove_temp_files.delay(
            video_file_path, watermark_file_path, output_video_path
        )  # Remove temp files

    except Exception as e:
        logger.error(str(e))
        raise Exception(str(e))

    finally:
        return True


@shared_task(bind=True, name="process_video_watermark")
def process_video_watermark(
    self, video_file_path, watermark_file_path, x_offset, y_offset, email, timestamp
):
    """
    Process video watermark
    """
    
    logger.info("Starting video watermarking...")

    try:
        process_video_util.delay(
            video_file_path,
            watermark_file_path,
            x_offset,
            y_offset,
            email,
            timestamp,
        )  # Add watermark

    except Exception as e:
        logger.error(str(e))
        raise Exception(str(e))

    finally:
        return True
