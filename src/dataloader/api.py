from fastapi import HTTPException, FastAPI
from pydantic import BaseModel
from typing import List

from dataloader.s3 import s3Manager
import dataloader.mongodb as mongodb

from fastapi import FastAPI
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from pprint import pprint
import dataloader.merge as merge

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
    debate = mongodb.mongodb_find_one_document(
        { "s3_prefix": request.prefix }, mongodb.MONGO_DEBATES_COLLECTION
    )
    debate_id = debate["_id"]
    speakers = mongodb.mongodb_find_one_document(
        { "debate_id": debate_id }, mongodb.MONGO_SPEAKERS_COLLECTION
    )
    segments = mongodb.mongodb_find_one_document(
        { "debate_id": debate_id }, mongodb.MONGO_SEGMENTS_COLLECTION
    )
    subtitles = mongodb.mongodb_find_one_document(
        { "debate_id": debate_id, "type": merge.SUBTITLE_TYPE_TRANSCRIPT }, mongodb.MONGO_SUBTITLE_COLLECTION
    )
    subtitles_en = mongodb.mongodb_find_one_document(
        { "debate_id": debate_id, "type": merge.SUBTITLE_TYPE_TRANSLATION }, mongodb.MONGO_SUBTITLE_COLLECTION
    )
    return {
        "debate": _clean_document(debate),
        "speakers": _clean_document(speakers),
        "segments": _clean_document(segments),
        "subtitles": _clean_document(subtitles),
        "subtitles_en": _clean_document(subtitles_en),
    }


def _clean_document(document):
    if "_id" in document.keys():
        document["_id"] = str(document["_id"])
    if "debate_id" in document.keys():
        document["debate_id"] = str(document["debate_id"])
    return document
