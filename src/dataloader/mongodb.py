import json
import os
import uuid
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")


def mongodb_insert_video(data, date):
    """Insert one video into the mongodb"""
    video_data = _get_video_data(data, date)
    video_id = _mongodb_insert_one(video_data)
    return video_id


def mongodb_find_video(version_id):
    """Find videos in the mongodb: currently all videos are returned"""
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        document = db[MONGO_COLLECTION].find_one({
            "version_id": version_id,
        })
    return document


def _mongodb_insert_one(video_data):
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        video_id = db[MONGO_COLLECTION].insert_one(video_data).inserted_id
        if video_id:
            return video_id


def _get_video_data(data, date):
    video_data = {
        "date": date,
        "speakers": _get_speakers(data),
        "segments": _get_segments(data),
        "subtitles": _get_subtitles(data),
        "video_s3_id": str(uuid.uuid4()),
        "version_id": str(uuid.uuid4()),
    }
    return video_data


def _get_list_from_cursor(cursor):
    document_list = []
    for document in cursor:
        document_list.append(document)
    return document_list


def _get_subtitles(data):
    subtitles = [{
        "index": subtitle["index"],
        "start": subtitle["start"],
        "end": subtitle["end"],
        "content": subtitle["content"],
        "segment_nr": subtitle["segment_nr"],
    } for subtitle in data]
    return subtitles


def _get_speakers(data):
    speaker_ids = {subtitle["speaker_id"] for subtitle in data}
    speakers = [{
        "speaker_id": speaker_id,
        "name": "",
        "country": "",
    } for speaker_id in speaker_ids]
    return speakers


def _get_segments(data):
    segment_nrs = {subtitle["segment_nr"] for subtitle in data}
    segments = []
    for i, segment_nr in enumerate(segment_nrs):
        segment = _get_segment(data, segment_nr)
        segments.append(segment)
    return segments

def _get_segment(data, segment_nr):
    subtitles_in_segment = [
        subtitle for subtitle in data if subtitle["segment_nr"] == segment_nr
    ]
    speaker_id = subtitles_in_segment[0]["speaker_id"]
    segment_nr = subtitles_in_segment[0]["segment_nr"]
    start = min([subtitle["start"] for subtitle in subtitles_in_segment])
    end = max([subtitle["end"] for subtitle in subtitles_in_segment])
    start_index = min([subtitle["index"] for subtitle in subtitles_in_segment])
    end_index = max([subtitle["index"] for subtitle in subtitles_in_segment])
    segment = {
        "speaker_id": speaker_id,
        "start": start,
        "end": end,
        "first_index": start_index,
        "last_index": end_index,
        "segment_nr": segment_nr,
    }
    return segment
