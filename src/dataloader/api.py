from fastapi import HTTPException, FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import List

from dataloader.s3 import s3Manager
import dataloader.mongodb as mongodb
import dataloader.solr as solr

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


class Speaker(BaseModel):
    speaker_id: str
    name: str
    role_tag: str


class Subtitle(BaseModel):
    index: int
    start: float
    end: float
    content: str
    speaker_id: str
    segment_nr: int


class Segment(BaseModel):
    speaker_id: str
    start: float
    end: float
    segment_nr: int


class UpdateSpeakersRequest(BaseModel):
    prefix: str
    speakers: List[Speaker]


class EnumSubtitleType(str, Enum):
    transcript = "Transcript"
    translation = "Translation"


class UpdateSubtitlesRequest(BaseModel):
    prefix: str
    segmentNr: int
    subtitles: List[Subtitle]
    subtitleType: EnumSubtitleType


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


@api.post("/update-speakers")
async def mongo_metadata(request: UpdateSpeakersRequest):
    """
    Update speakers
    """
    debate = mongodb.mongodb_find_one_document(
        { "s3_prefix": request.prefix }, mongodb.MONGO_DEBATES_COLLECTION
    )
    debate_id = debate["_id"]
    speakers_as_dicts = [speaker.dict() for speaker in request.speakers]
    mongodb.update_document(
        query={ "debate_id": debate_id },
        values={ "$set": { "speakers": speakers_as_dicts } },
        collection=mongodb.MONGO_SPEAKERS_COLLECTION
    )
    print(f"speakers for {request.prefix} have been updated on mongodb")
    solr.update_speakers(s3_prefix=request.prefix, speakers=speakers_as_dicts)
    print(f"speakers for {request.prefix} have been updated on solr")


@api.post("/update-subtitles")
async def mongo_metadata(request: UpdateSubtitlesRequest):
    """
    Update subtitles
    """
    print("in update subtitles")
    print(request)
    debate = mongodb.mongodb_find_one_document(
        { "s3_prefix": request.prefix }, mongodb.MONGO_DEBATES_COLLECTION
    )
    debate_id = debate["_id"]
    subtitles_as_dicts = [subtitle.dict() for subtitle in request.subtitles]
    if request.subtitleType == EnumSubtitleType.transcript:
        values = { "subtitles": subtitles_as_dicts }
    else:
        values = { "subtitles_en": subtitles_as_dicts }
    if request.subtitleType == EnumSubtitleType.transcript:
        subtitle_type = merge.SUBTITLE_TYPE_TRANSCRIPT
    elif request.subtitleType == EnumSubtitleType.translation:
        subtitle_type = merge.SUBTITLE_TYPE_TRANSLATION
    mongodb.update_document(
        query={ "debate_id": debate_id, "type": subtitle_type },
        values={ "$set": values },
        collection=mongodb.MONGO_SUBTITLE_COLLECTION,
    )
    print(f"subtitles for {request.prefix} have been updated on mongodb")
    solr.update_segment(
        s3_prefix=request.prefix,
        segment_nr=request.segmentNr,
        subtitles=subtitles_as_dicts,
        subtitle_type=subtitle_type,
    )
    print(f"subtitles for {request.prefix} have been updated on solr")


def _clean_document(document):
    if "_id" in document.keys():
        document["_id"] = str(document["_id"])
    if "debate_id" in document.keys():
        document["debate_id"] = str(document["debate_id"])
    return document
