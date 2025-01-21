import json
import os
import uuid
from bson import ObjectId
import importlib.resources as resources
from datetime import datetime, timezone
import pytz
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_DEBATES_COLLECTION = os.getenv("MONGO_DEBATES_COLLECTION")
ZURICH_TZ = pytz.timezone('Europe/Zurich')
LANGUAGE_ENGLISH = "en"


class DataloaderMongoException(Exception):
    pass


def _get_schema():
    with resources.open_text("dataloader", "schema_mongo_validator.json") as file:
        schema = json.load(file)
        return schema


def mongodb_test_connection():
    with MongoClient(MONGO_URL, serverSelectionTimeoutMS = 2000) as client:
        print(client.server_info())


def mongodb_create_debate_collection_with_schema():
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        schema = _get_schema()
        result = db.create_collection(schema["collection"], validator=schema["validator"])
        print(result)


def mongodb_insert_debate(data_orig, data_en, metadata):
    """Insert one debate into the mongodb"""
    debate_data = _get_debate_data(
        data_orig=data_orig, data_en=data_en, metadata=metadata
    )
    try:
        debate_data_db = _get_document_by_id(debate_id)
    except Exception as e:
        pass
    debate_id = _mongodb_insert_one(debate_data)
    print(f"Successfully inserted debate into mongodb with id: {debate_id}")
    debate_data_db = _get_document_by_id(debate_id)
    return debate_data_db


def mongodb_find_debates():
    """Find debates in MongoDB and return s3_prefix and version_id."""
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        query = {}
        projection = {"s3_prefix", "version_id"}
        result = db[MONGO_DEBATES_COLLECTION].find(query, projection)
        return _get_list_from_cursor(result)


def _get_document_by_id(document_id):
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        document = db[MONGO_DEBATES_COLLECTION].find_one({"_id": ObjectId(document_id)})
        return document


def mongodb_find_one_debate(s3_prefix, version_id=None):
    """Find debates in MongoDB and return s3_prefix and version_id."""
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        query = {"s3_prefix": s3_prefix}
        if version_id:
            query["version_id"] = version_id
        document = db[MONGO_DEBATES_COLLECTION].find_one(query)
        return document


def _mongodb_insert_one(debate_data):
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        debate_id = db[MONGO_DEBATES_COLLECTION].insert_one(
            debate_data
        ).inserted_id
        return debate_id


def mongodb_delete_debates():
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        db.drop_collection(MONGO_DEBATES_COLLECTION)


def _get_debate_data(data_orig, data_en, metadata):
    debate_data = {
        "s3_prefix": metadata["s3_prefix"],
        "version": _get_version(),
        "s3_keys": metadata["s3_keys"],
        "created_at": _format_current_datetime(),
        "debate": _get_debate(metadata),
        "speakers": _get_speakers(data_orig),
        "segments": _get_segments(data_orig),
        "subtitles": _get_subtitles(data_orig),
        "subtitles_en": _get_subtitles(data_en, language=LANGUAGE_ENGLISH),
        "s3_keys": metadata["s3_keys"],
        "media": metadata["media"],
    }
    return debate_data

def _get_version():
    version = {
        "version_id": str(uuid.uuid4()),
        "original": True
    }
    return version



def _get_list_from_cursor(cursor):
    document_list = []
    for document in cursor:
        document_list.append(document)
    return document_list


def _get_debate(metadata):
    debate = {
      "schedule": _format_debate_schedule(metadata["schedule"]),
      "public": metadata["context"]["public"],
      "type": metadata["context"]["type"],
      "session": metadata["context"]["session"],
    }
    return debate


def _get_subtitles(data, language=None):
    subtitles = []
    for item in data:
        subtitle = {
            "index": item["index"],
            "start": item["start"],
            "end": item["end"],
            "content": item["content"],
            "segment_nr": item["segment_nr"],
        }
        if language:
            subtitle["language"] = language
        else:
            subtitle["language"] = ""
        subtitles.append(subtitle)
    return subtitles


def _get_speakers(data_orig):
    speaker_ids = {subtitle["speaker_id"] for subtitle in data_orig}
    speakers = [{
        "speaker_id": speaker_id,
        "name": "",
        "role_tag": "",
    } for speaker_id in speaker_ids]
    return speakers


def _get_segments(data_orig):
    segment_nrs = {subtitle["segment_nr"] for subtitle in data_orig}
    segments = []
    for i, segment_nr in enumerate(segment_nrs):
        segment = _get_segment(data_orig, segment_nr)
        segments.append(segment)
    return segments


def _get_segment(data_orig, segment_nr):
    subtitles_in_segment = [
        subtitle for subtitle in data_orig if subtitle["segment_nr"] == segment_nr
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


def _format_debate_schedule(schedule):
    datetime_str = f"{schedule['date']} {schedule['time']}"
    naive_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    timezone_obj = pytz.timezone(schedule["timezone"])
    localized_datetime = timezone_obj.localize(naive_datetime)
    utc_datetime = localized_datetime.astimezone(pytz.UTC)
    return _format_date(utc_datetime)


def _format_current_datetime():
    current_datetime = datetime.now(
        timezone.utc
    )
    return _format_date(current_datetime)


def _format_date(dt):
    return dt.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
