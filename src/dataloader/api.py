from fastapi import HTTPException, FastAPI
from pydantic import BaseModel
from typing import List

from dataloader.s3 import s3Manager
from dataloader.mongodb import mongodb_find_one_debate

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pprint import pprint

api = FastAPI()


# Set CORS policy to allow your frontend's origin
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class S3MediaUrlRequest(BaseModel):
    prefix: str
    objectKeys: list[str]
    mediaKey: str


class S3MediaUrls(BaseModel):
    url: str
    label: str


class S3MediaUrlResponse(BaseModel):
    signedUrls: List[S3MediaUrls]
    signedMediaUrl: str


class S3MetadataRequest(BaseModel):
    prefix: str


@api.post("/get-media-urls")
async def get_media_urls(request: S3MediaUrlRequest):
    s3_client = s3Manager()
    presigned_urls = []
    for object_key in request.objectKeys:
        url = s3_client.get_presigned_url(request.prefix, object_key)
        presigned_urls.append({
            "url": url,
            "label": object_key,
        })

        response = {}
        response["signedUrls"] = presigned_urls

        filter_media_url = [item["url"]
                     for item in presigned_urls
                     if item["label"] == request.mediaKey]
        if filter_media_url:
            media_url = filter_media_url[0]
        else:
            media_url = s3_client.get_presigned_url(request.prefix, object_key)
        response["signedMediaUrl"] = media_url
        pprint(response)

    return response


@api.post("/mongo-metadata")
async def mongo_metadata(request: S3MetadataRequest):
    """
    Get Metadata for Debates Object
    """
    try:
        document = mongodb_find_one_debate(request.prefix)
        document["_id"] = str(document["_id"])
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        print(e)
    return {
        "success": True,
        "data": document,
    }
