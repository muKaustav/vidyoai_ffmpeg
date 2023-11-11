from fastapi import FastAPI
from routes.user import user
from routes.audio import audio
from routes.video import video

app = FastAPI()

app.include_router(user, prefix="/user", tags=["user"])
app.include_router(audio, prefix="/audio", tags=["audio"])
app.include_router(video, prefix="/video", tags=["video"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
