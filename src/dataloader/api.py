from fastapi import HTTPException, FastAPI
from pydantic import BaseModel

from dataloader.s3 import s3Manager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI()


# Set CORS policy to allow your frontend's origin
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class S3PrefixRequest(BaseModel):
    prefix: str  # Common prefix to derive video and subtitle keys
    expiration: int = 3600  # Default expiration time for the URLs (in seconds)


@api.post("/get-media-urls")
async def get_media_urls(request: S3PrefixRequest):
    print("route reached: deriving media urls")
    s3_client = s3Manager()
    media_urls = s3_client.get_video_presigned_urls(request.prefix)
    print(media_urls)
    if not media_urls:
        raise HTTPException(status_code=500, detail="Failed to generate media presigned URLs")
    return {
        "video_url": media_urls["video_url"],
        "subtitle_url": media_urls["subtitle_url"],
    }
