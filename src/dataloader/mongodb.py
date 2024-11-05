import json
import os
import uuid
import importlib.resources as resources
from datetime import datetime, timezone
import pytz
from pprint import pprint
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_VIDEO_COLLECTION = os.getenv("MONGO_VIDEO_COLLECTION")
ZURICH_TZ = pytz.timezone('Europe/Zurich')


def _get_schema():
    with resources.open_text("dataloader", "schema_mongo_validator.json") as file:
        schema = json.load(file)
        return schema


def mongodb_test_connection():
    with MongoClient(MONGO_URL, serverSelectionTimeoutMS = 2000) as client:
        return client.server_info()


def mongodb_create_video_collection_with_schema():
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        schema = _get_schema()
        result = db.create_collection(schema["collection"], validator=schema["validator"])
        print(result)


def mongodb_insert_video(data, metadata):
    """Insert one video into the mongodb"""
    video_data = _get_video_data(data, metadata)
    video_id = _mongodb_insert_one(video_data)
    return video_id


def mongodb_find_videos():
    """Find videos in MongoDB and return s3_prefix and version_id."""
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        query = {}
        projection = {"s3_prefix", "version_id"}
        result = db[MONGO_VIDEO_COLLECTION].find(query, projection)
        return _get_list_from_cursor(result)


def mongodb_find_one_video(s3_prefix, version_id):
    """Find videos in MongoDB and return s3_prefix and version_id."""
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        query = {"s3_prefix": s3_prefix, "version_id": version_id}
        document = db[MONGO_VIDEO_COLLECTION].find_one(query)
        return document


def _mongodb_insert_one(video_data):
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        result = db[MONGO_VIDEO_COLLECTION].insert_one(
            video_data
        ).inserted_id
        pprint(result)


def mongodb_delete_videos():
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        db.drop_collection(MONGO_VIDEO_COLLECTION)


def _get_video_data(data, metadata):
    video_data = {
        "s3_prefix": metadata["video"]["s3_prefix"],
        "version_id": str(uuid.uuid4()),
        "created_at": datetime.now(ZURICH_TZ).isoformat(),
        "debate": _get_debate(metadata),
        "speakers": _get_speakers(data),
        "segments": _get_segments(data),
        "subtitles": _get_subtitles(data),
    }
    return video_data


def _get_list_from_cursor(cursor):
    document_list = []
    for document in cursor:
        document_list.append(document)
    return document_list


def _get_debate(metadata):
    debate = {
      "schedule": _transform_schedule_into_isodate(metadata["schedule"]),
      "type": metadata["context"]["type"],
      "session": metadata["context"]["session"],
      "topic": metadata["context"]["topic"],
      "public": metadata["context"]["public"],
    }
    return debate


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
        "role": "",
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
    segment = {
        "speaker_id": speaker_id,
        "start": start,
        "end": end,
        "segment_nr": segment_nr,
    }
    return segment


def _transform_schedule_into_isodate(schedule):
    datetime_str = f"{schedule['date']} {schedule['time']}"
    naive_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    timezone_obj = pytz.timezone(schedule["timezone"])
    localized_datetime = timezone_obj.localize(naive_datetime)
    zh_datetime = localized_datetime.astimezone(ZURICH_TZ)
    return zh_datetime.isoformat()
